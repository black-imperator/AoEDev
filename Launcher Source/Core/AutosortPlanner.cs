using System;
using System.Collections.Generic;
using System.Linq;
using AoELauncher.Models;

namespace AoELauncher.Core;

/// One module that autosort wants to move to a different Load #, and why.
public sealed class AutosortMove
{
    public ModuleInfo Module { get; set; } = new();
    public string FromPass { get; set; } = "";
    public string ToPass { get; set; } = "";

    /// Short explanation, e.g. "must load after 'Some Folder'".
    public string Reason { get; set; } = "";
}

/// The outcome of AutosortPlanner.Plan(): either a list of moves (possibly empty, meaning the
/// order is already fine) or a reason why no solution was found.
public sealed class AutosortPlan
{
    public string? FailureReason { get; set; }
    public bool Success => FailureReason == null;
    public List<AutosortMove> Moves { get; } = new();
}

/// A deliberately simple, greedy "Autosort" for the active modules. It only ever changes the
/// Load # of modules, and only to satisfy [dependency-hard] / [dependency-soft] load order: a
/// dependency must load strictly before the module that lists it (lower Load #, or the same
/// Load # and earlier alphabetically by folder name -- see ModuleChecker).
///
/// Assumptions it is built around:
///  - few modules have dependencies, and dependency chains are short;
///  - most modules should stay in the Load # they are already in, so only modules involved in a
///    broken dependency are ever moved;
///  - anything unusual (a dependency loop, chains too long for Load # 0-4, any unexpected error)
///    is not handled cleverly: planning just fails with a message and the user fixes it by hand.
///
/// Method: the dependencies form a graph; if it contains a loop there is no valid order, so give
/// up. Otherwise two greedy solutions are built and the one that disturbs fewer modules wins:
///   A) walk the modules dependencies-first; a module keeps its Load # unless one of its
///      dependencies would load too late, in which case it is pushed to the earliest Load # that
///      works (dependents move later, dependencies stay put);
///   B) walk the modules dependents-first; a module keeps its Load # unless one of its
///      dependents would load too early, in which case it is pulled to the latest Load # that
///      works (dependencies move earlier, dependents stay put).
/// Each solution is valid by construction (and is re-verified at the end); either may fail by
/// running out of Load #s, in which case the other is used.
///
/// Plan() is a dry run that touches no files. The caller shows the moves for confirmation and
/// then performs them.
public static class AutosortPlanner
{
    private sealed class Node
    {
        public LoadEntry Entry = null!;
        public string Folder = "";
        public int Start;

        /// Modules this one needs to load before itself (hard and soft dependencies that are in the set).
        public List<Node> Deps = new();

        /// The reverse of Deps.
        public List<Node> Dependents = new();

        public int FinalA, FinalB;
        public string ReasonA = "", ReasonB = "";
    }

    public static AutosortPlan Plan(IReadOnlyList<LoadEntry> set)
    {
        var plan = new AutosortPlan();
        try
        {
            PlanCore(set, plan);
        }
        catch (Exception ex)
        {
            plan.Moves.Clear();
            plan.FailureReason = "An unexpected error occurred while working out a solution: " + ex.Message;
        }
        return plan;
    }

    private static bool LoadsEarlierByName(Node first, Node second) =>
        string.Compare(first.Folder, second.Folder, StringComparison.OrdinalIgnoreCase) < 0;

    private static string Quote(Node n) => $"'{n.Entry.Module.Name}'";

    private static void PlanCore(IReadOnlyList<LoadEntry> set, AutosortPlan plan)
    {
        int max = ModuleLayout.MaxPass;

        // --- Build the dependency graph over the modules in the set ---------------------------
        var byFolder = new Dictionary<string, Node>(StringComparer.OrdinalIgnoreCase);
        var nodes = new List<Node>();
        foreach (var entry in set)
        {
            var node = new Node
            {
                Entry = entry,
                Folder = entry.Module.FolderName,
                Start = ModuleLayout.PassIndex(entry.Pass),
            };
            if (byFolder.ContainsKey(node.Folder)) continue; // folder names are unique on a side; ignore a stray duplicate
            byFolder[node.Folder] = node;
            nodes.Add(node);
        }

        foreach (var node in nodes)
        {
            foreach (var depFolder in node.Entry.Module.Dependencies.Concat(node.Entry.Module.SoftDependencies))
            {
                if (!byFolder.TryGetValue(depFolder, out var dep) || ReferenceEquals(dep, node)) continue;
                if (node.Deps.Contains(dep)) continue; // listed as both hard and soft
                node.Deps.Add(dep);
                dep.Dependents.Add(node);
            }
        }

        // --- Dependencies-first order; leftovers mean a dependency loop -----------------------
        var order = new List<Node>();
        var done = new HashSet<Node>();
        while (order.Count < nodes.Count)
        {
            var next = nodes
                .Where(n => !done.Contains(n) && n.Deps.All(done.Contains))
                .OrderBy(n => n.Folder, StringComparer.OrdinalIgnoreCase)
                .FirstOrDefault();
            if (next == null)
            {
                plan.FailureReason = DescribeLoop(nodes.Where(n => !done.Contains(n)).ToList());
                return;
            }
            order.Add(next);
            done.Add(next);
        }

        // --- Solution A: push dependents later ------------------------------------------------
        Node? failedA = null;
        int failedAWanted = 0;
        foreach (var node in order)
        {
            int need = 0;
            Node? binding = null;
            foreach (var dep in node.Deps)
            {
                int required = LoadsEarlierByName(dep, node) ? dep.FinalA : dep.FinalA + 1;
                if (required > need) { need = required; binding = dep; }
            }

            node.FinalA = Math.Max(node.Start, need);
            if (node.FinalA > node.Start && binding != null)
                node.ReasonA = $"must load after {Quote(binding)}";

            if (node.FinalA > max && failedA == null)
            {
                failedA = node;
                failedAWanted = node.FinalA;
            }
        }
        bool aOk = failedA == null;

        // --- Solution B: pull dependencies earlier --------------------------------------------
        Node? failedB = null;
        for (int i = order.Count - 1; i >= 0; i--)
        {
            var node = order[i];
            int limit = max;
            Node? binding = null;
            foreach (var dependent in node.Dependents)
            {
                int allowed = LoadsEarlierByName(node, dependent) ? dependent.FinalB : dependent.FinalB - 1;
                if (allowed < limit) { limit = allowed; binding = dependent; }
            }

            node.FinalB = Math.Min(node.Start, limit);
            if (node.FinalB < node.Start && binding != null)
                node.ReasonB = $"must load before {Quote(binding)}";

            if (node.FinalB < 0 && failedB == null)
                failedB = node;
        }
        bool bOk = failedB == null;

        if (!aOk && !bOk)
        {
            plan.FailureReason =
                $"The dependency chains don't fit in the {ModuleLayout.Passes.Length} available Load #s " +
                $"({ModuleLayout.Passes[0]}-{ModuleLayout.Passes[max]}): moving modules later would need " +
                $"{Quote(failedA!)} to be in Load #{failedAWanted} (past the last one), and moving modules earlier " +
                $"would need {Quote(failedB!)} to be placed before Load #{ModuleLayout.Passes[0]}.";
            return;
        }

        // --- Pick the solution that disturbs fewer modules (then moves them less far) ---------
        int MovedCount(Func<Node, int> final) => nodes.Count(n => final(n) != n.Start);
        int Distance(Func<Node, int> final) => nodes.Sum(n => Math.Abs(final(n) - n.Start));

        bool useA;
        if (aOk && bOk)
        {
            int countA = MovedCount(n => n.FinalA), countB = MovedCount(n => n.FinalB);
            useA = countA != countB ? countA < countB : Distance(n => n.FinalA) <= Distance(n => n.FinalB);
        }
        else
        {
            useA = aOk;
        }

        Func<Node, int> chosen;
        if (useA) chosen = n => n.FinalA;
        else chosen = n => n.FinalB;

        // --- Safety net: confirm every dependency really is satisfied by the chosen result ----
        foreach (var node in nodes)
        {
            foreach (var dep in node.Deps)
            {
                int d = chosen(dep), m = chosen(node);
                bool satisfied = d < m || (d == m && LoadsEarlierByName(dep, node));
                if (!satisfied)
                {
                    plan.FailureReason =
                        $"The result for {Quote(node)} and {Quote(dep)} didn't check out, so nothing was changed.";
                    return;
                }
            }
        }

        foreach (var node in nodes.OrderBy(n => n.Entry.Module.Name, StringComparer.OrdinalIgnoreCase))
        {
            int to = chosen(node);
            if (to == node.Start) continue;
            plan.Moves.Add(new AutosortMove
            {
                Module = node.Entry.Module,
                FromPass = ModuleLayout.PassFromIndex(node.Start),
                ToPass = ModuleLayout.PassFromIndex(to),
                Reason = useA ? node.ReasonA : node.ReasonB,
            });
        }
    }

    /// Names a loop among the leftover modules. Every leftover module has at least one leftover
    /// dependency, so walking from any of them along leftover dependencies must come back around.
    private static string DescribeLoop(List<Node> leftover)
    {
        var remaining = new HashSet<Node>(leftover);
        var path = new List<Node>();
        var current = leftover[0];

        while (!path.Contains(current))
        {
            path.Add(current);
            current = current.Deps.First(remaining.Contains);
        }

        var loop = path.Skip(path.IndexOf(current)).ToList();
        var names = string.Join(" -> ", loop.Concat(new[] { loop[0] }).Select(Quote));
        return "Some modules depend on each other in a loop, so no order can satisfy all of them: " + names + ".";
    }
}
