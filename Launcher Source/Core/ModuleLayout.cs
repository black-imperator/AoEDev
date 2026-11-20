using System;
using System.Collections.Generic;
using System.IO;

namespace AoELauncher.Core;

/// The one place that knows how module folders are laid out on disk. For both
/// the active and inactive side the structure is:
///
///   Assets\Modules\0..4\<module>              Assets\Modules (Off)\0..4\<module>
///
/// A module's "Load #" is the number of the folder it lives in (0 to 4). The game loads
/// Load # 0 first, then 1, 2, 3, 4; within each folder modules load alphabetically by module
/// folder name. Moving a module between the active and inactive sides preserves its Load #
/// (see MainForm.PerformMoves).
public static class ModuleLayout
{
    /// The Load # that newly installed modules (e.g. dropped in from Explorer) start in, and the
    /// one used wherever a Load # is missing or invalid.
    public const string DefaultPass = "1";

    /// Every valid Load #, in the order the game loads them. The text of each entry is its own index.
    public static readonly string[] Passes = { "0", "1", "2", "3", "4" };

    /// The highest valid Load #.
    public static int MaxPass => Passes.Length - 1;

    public static string GetSideRoot(string modPath, bool active) =>
        Path.Combine(modPath, "Assets", active ? "Modules" : "Modules (Off)");

    public static string GetPassDir(string modPath, bool active, string pass)
    {
        var p = NormalizePass(pass);
        if (p.Length == 0) p = DefaultPass;
        return Path.Combine(GetSideRoot(modPath, active), p);
    }

    /// Returns the canonical Load # ("0".."4"), or "" if the input isn't a valid one.
    public static string NormalizePass(string? pass)
    {
        var p = (pass ?? "").Trim();
        foreach (var valid in Passes)
            if (string.Equals(p, valid, StringComparison.Ordinal))
                return valid;
        return "";
    }

    /// The text shown to the user for a Load #: the number itself.
    public static string PassDisplayName(string? pass)
    {
        var p = NormalizePass(pass);
        return p.Length > 0 ? p : DefaultPass;
    }

    /// "Load #2" -- a Load # as written inside sentences.
    public static string PassLabel(string? pass) => "Load #" + PassDisplayName(pass);

    /// Position of a Load # in the game's load sequence (0..4). Unknown values count as the default.
    public static int PassIndex(string? pass) => Array.IndexOf(Passes, PassDisplayName(pass));

    /// The Load # for a given sequence position (0..4), or "" if it is out of range.
    public static string PassFromIndex(int index) =>
        index >= 0 && index < Passes.Length ? Passes[index] : "";

    /// Works out a module folder's Load # from where it sits: ...\N\<module> is Load # N.
    /// Anything else counts as the default.
    public static string GetPassFromPath(string moduleDir)
    {
        var trimmed = moduleDir.TrimEnd(Path.DirectorySeparatorChar, Path.AltDirectorySeparatorChar);
        var parent = Path.GetDirectoryName(trimmed);
        if (string.IsNullOrEmpty(parent)) return DefaultPass;

        var p = NormalizePass(Path.GetFileName(parent));
        return p.Length > 0 ? p : DefaultPass;
    }

    /// Every existing folder with this module folder name anywhere on the given side (Load # 0..4).
    public static List<string> FindOnSide(string modPath, bool active, string name)
    {
        var found = new List<string>();
        foreach (var pass in Passes)
        {
            var candidate = Path.Combine(GetPassDir(modPath, active, pass), name);
            if (Directory.Exists(candidate)) found.Add(candidate);
        }
        return found;
    }
}
