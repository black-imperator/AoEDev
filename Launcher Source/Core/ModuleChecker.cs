using System;
using System.Collections.Generic;
using System.Linq;
using AoELauncher.Models;

namespace AoELauncher.Core;

/// A module as it would be loaded: its scan info plus the Load # it would load in. The Load # is
/// kept separate from ModuleInfo.LoadPass so a preset (which records its own Load #s) can be
/// checked without moving any folders.
public sealed class LoadEntry
{
    public ModuleInfo Module { get; }
    public string Pass { get; }

    public LoadEntry(ModuleInfo module, string pass)
    {
        Module = module;
        var normalized = ModuleLayout.NormalizePass(pass);
        Pass = normalized.Length > 0 ? normalized : module.LoadPass;
    }
}

/// Hard dependency problems, split by kind: a dependency that isn't in the set at all can only be
/// fixed by activating (or installing) it, while one that is present but loads too late is a
/// load order problem. Each entry is a ready-to-show block of text for one module.
public sealed class DependencyIssues
{
    public List<string> Missing { get; } = new();
    public List<string> Misordered { get; } = new();
}

/// Everything wrong with a set of modules, grouped the way the launcher reports it:
/// "module issues" (incompatibilities and missing hard dependencies) versus "order issues"
/// (a hard or soft dependency that is present but loads after the module that needs it).
public sealed class SetAnalysis
{
    public List<string> Incompatible { get; set; } = new();
    public List<string> MissingDependencies { get; set; } = new();
    public List<string> HardOrderIssues { get; set; } = new();
    public List<string> SoftOrderIssues { get; set; } = new();

    public bool HasModuleIssue => Incompatible.Count > 0 || MissingDependencies.Count > 0;
    public bool HasOrderIssue => HardOrderIssues.Count > 0 || SoftOrderIssues.Count > 0;
}

/// Verifies a set of modules that is about to be used (launched, saved or exported):
///  - [incompatible]: no module in the set may list another module in the set as incompatible.
///  - [dependency-hard]: every module listed under a module's [dependency-hard] must be in the set
///    AND load before it.
///  - [dependency-soft]: modules listed under a module's [dependency-soft] need not be in the set,
///    but any that ARE must load before it.
///
/// The game loads Load # 0 first, then 1, 2, 3, 4; within each Load # modules load
/// alphabetically by module folder name. Modules are referred to in [dependency] / [incompatible]
/// by their exact FOLDER name (not their [name] entry), matched case-insensitively; folder names
/// are unique on a side, so a reference can never be ambiguous.
public static class ModuleChecker
{
    private static readonly StringComparer NameComparer = StringComparer.OrdinalIgnoreCase;

    /// "'Folder'" when the display name is the same, otherwise "'Display Name' (folder 'Folder')".
    private static string Describe(ModuleInfo m) =>
        string.Equals(m.Name, m.FolderName, StringComparison.Ordinal)
            ? $"'{m.FolderName}'"
            : $"'{m.Name}' (folder '{m.FolderName}')";

    /// Runs every check on the set and groups the results.
    public static SetAnalysis Analyze(IReadOnlyList<LoadEntry> set, IEnumerable<ModuleInfo> installed, string notInSetPhrase)
    {
        var deps = CheckDependencies(set, installed, notInSetPhrase);
        return new SetAnalysis
        {
            Incompatible = CheckIncompatibilities(set),
            MissingDependencies = deps.Missing,
            HardOrderIssues = deps.Misordered,
            SoftOrderIssues = CheckSoftDependencies(set),
        };
    }

    /// Returns one entry per incompatible pair found in the set (empty if there are none).
    public static List<string> CheckIncompatibilities(IReadOnlyList<LoadEntry> set)
    {
        var issues = new List<string>();
        var reported = new HashSet<string>(StringComparer.Ordinal);

        foreach (var a in set)
        {
            foreach (var badFolder in a.Module.Incompatible)
            {
                foreach (var b in set)
                {
                    if (ReferenceEquals(a, b) || !NameComparer.Equals(b.Module.FolderName, badFolder))
                        continue;

                    // Report each pair once, even if both modules list each other.
                    var first = a.Module.FolderName.ToLowerInvariant();
                    var second = b.Module.FolderName.ToLowerInvariant();
                    var key = string.CompareOrdinal(first, second) <= 0 ? first + "|" + second : second + "|" + first;
                    if (!reported.Add(key)) continue;

                    var mutual = b.Module.Incompatible.Any(n => NameComparer.Equals(n, a.Module.FolderName));
                    issues.Add(mutual
                        ? $"{Describe(a.Module)} and {Describe(b.Module)} each list the other as incompatible."
                        : $"{Describe(a.Module)} lists {Describe(b.Module)} as incompatible.");
                }
            }
        }

        return issues;
    }

    /// Checks every module's hard dependencies. A module with a dependency that isn't in the set
    /// goes into Missing; one whose dependency is in the set but loads after it goes into
    /// Misordered (a module can appear in both).
    /// `installed` is every module found on disk (either side); it only serves to word the message
    /// ("installed but not active" versus "not installed"). `notInSetPhrase` completes the sentence
    /// "...which is not ___", e.g. "active" or "in the preset".
    public static DependencyIssues CheckDependencies(
        IReadOnlyList<LoadEntry> set, IEnumerable<ModuleInfo> installed, string notInSetPhrase)
    {
        var issues = new DependencyIssues();
        var installedList = installed.ToList();

        foreach (var entry in set.OrderBy(e => e, new LoadOrderComparer()))
        {
            var missing = new List<string>();
            var misordered = new List<string>();

            foreach (var depFolder in entry.Module.Dependencies)
            {
                if (NameComparer.Equals(depFolder, entry.Module.FolderName))
                    continue; // a module can't meaningfully depend on itself

                var candidates = set
                    .Where(c => !ReferenceEquals(c, entry) && NameComparer.Equals(c.Module.FolderName, depFolder))
                    .ToList();

                if (candidates.Count == 0)
                {
                    var onDisk = installedList.Any(m => NameComparer.Equals(m.FolderName, depFolder));
                    missing.Add(onDisk
                        ? $"requires '{depFolder}', which is installed but not {notInSetPhrase}."
                        : $"requires '{depFolder}', which is not installed.");
                    continue;
                }

                var dep = candidates[0];
                if (LoadsBefore(dep, entry))
                    continue; // satisfied

                misordered.Add($"requires {Describe(dep.Module)}, but {OrderExplanation(dep, entry)}");
            }

            if (missing.Count > 0) issues.Missing.Add(FormatModuleBlock(entry, missing));
            if (misordered.Count > 0) issues.Misordered.Add(FormatModuleBlock(entry, misordered));
        }

        return issues;
    }

    private static string FormatModuleBlock(LoadEntry entry, IEnumerable<string> problems) =>
        $"{Describe(entry.Module)} ({ModuleLayout.PassLabel(entry.Pass)}):\n" +
        string.Join("\n", problems.Select(p => "   - " + p));

    /// "it loads after this module (...)" with the reason spelled out (different Load #s, or the
    /// alphabetical order within one Load #).
    private static string OrderExplanation(LoadEntry dep, LoadEntry entry)
    {
        if (dep.Pass != entry.Pass)
            return "it loads after this module " +
                   $"(it is in {ModuleLayout.PassLabel(dep.Pass)}, " +
                   $"this module is in {ModuleLayout.PassLabel(entry.Pass)}).";

        return "it loads after this module " +
               $"(both are in {ModuleLayout.PassLabel(entry.Pass)}, where modules load " +
               $"alphabetically by folder name, and folder '{dep.Module.FolderName}' comes after " +
               $"'{entry.Module.FolderName}').";
    }

    /// Returns one entry per module that lists a [dependency-soft] module which is in the set but
    /// loads AFTER it (empty if the order is right everywhere). A soft dependency that is not in
    /// the set is fine and never reported.
    public static List<string> CheckSoftDependencies(IReadOnlyList<LoadEntry> set)
    {
        var issues = new List<string>();

        foreach (var entry in set.OrderBy(e => e, new LoadOrderComparer()))
        {
            var problems = new List<string>();

            foreach (var softFolder in entry.Module.SoftDependencies)
            {
                if (NameComparer.Equals(softFolder, entry.Module.FolderName))
                    continue;

                var dep = set.FirstOrDefault(c => !ReferenceEquals(c, entry) &&
                                                  NameComparer.Equals(c.Module.FolderName, softFolder));
                if (dep == null || LoadsBefore(dep, entry))
                    continue; // not loaded at all, or loaded in the right order

                problems.Add($"supports {Describe(dep.Module)}, which should load before it, but {OrderExplanation(dep, entry)}");
            }

            if (problems.Count > 0) issues.Add(FormatModuleBlock(entry, problems));
        }

        return issues;
    }

    /// True if `first` is loaded strictly before `second`.
    private static bool LoadsBefore(LoadEntry first, LoadEntry second) =>
        new LoadOrderComparer().Compare(first, second) < 0;

    /// Game load order: by Load # (0..4), then alphabetically by module folder name.
    /// Also used to list the report in the order the modules load.
    private sealed class LoadOrderComparer : IComparer<LoadEntry>
    {
        public int Compare(LoadEntry? x, LoadEntry? y)
        {
            if (x == null || y == null) return 0;
            var byPass = ModuleLayout.PassIndex(x.Pass).CompareTo(ModuleLayout.PassIndex(y.Pass));
            return byPass != 0
                ? byPass
                : string.Compare(x.Module.FolderName, y.Module.FolderName, StringComparison.OrdinalIgnoreCase);
        }
    }
}
