using System.Collections.Generic;

namespace AoELauncher.Models;

/// Represents a module folder as currently found on disk (either active or
/// inactive), including everything parsed out of its info.txt.
public class ModuleInfo
{
    /// The name shown to the user: the [name] entry of info.txt, or the folder name if that is missing or blank.
    /// This is also the name other modules use in their [dependency] and [incompatible] lists.
    public string Name { get; set; } = "";

    /// The module's folder name on disk. This is what the file system operations, presets and the
    /// game's load order use.
    public string FolderName { get; set; } = "";
    public string FullPath { get; set; } = "";
    public bool IsActive { get; set; }

    /// "Def" if stored under Def\, otherwise "1".."4" for Seq\1..4 (see Core/ModuleLayout).
    public string LoadPass { get; set; } = "Def";

    // --- from info.txt ---
    public string Version { get; set; } = "unknown";

    /// The Ashes of Erebus revision this module targets, from the [aoeversion] section (blank if absent).
    public string AoeRev { get; set; } = "";

    /// Tokens from the [tags] section, compared case-insensitively (e.g. "civ", "mech", "art", "joke").
    public HashSet<string> Tags { get; set; } = new(System.StringComparer.OrdinalIgnoreCase);
    public string Author { get; set; } = "";
    public List<string> Compatible { get; set; } = new();

    /// [name] entries of the modules that must be active and load before this one (from [dependency]).
    public List<string> Dependencies { get; set; } = new();

    /// [name] entries of the modules that must not be active at the same time as this one (from [incompatible]).
    public List<string> Incompatible { get; set; } = new();

    /// Shown as a tooltip when hovering the module row.
    public string ShortDesc { get; set; } = "";

    /// Shown in the popup when the "?" button on the row is clicked.
    public string Desc { get; set; } = "";
}
