using System.Collections.Generic;

namespace AoELauncher.Models;

/// Represents a module folder as currently found on disk (either active or
/// inactive), including everything parsed out of its info.txt.
public class ModuleInfo
{
    /// The name shown to the user: the [name] entry of info.txt, or the folder name if that is missing or blank.
    public string Name { get; set; } = "";

    /// The module's folder name on disk. This is what the file system operations, presets and the
    /// game's load order use.
    public string FolderName { get; set; } = "";
    public string FullPath { get; set; } = "";
    public bool IsActive { get; set; }

    /// The module's Load #, "0".."4": the number of the folder it is stored in (see Core/ModuleLayout).
    public string LoadPass { get; set; } = "1";

    // --- from info.txt ---
    public string Version { get; set; } = "unknown";

    /// The Ashes of Erebus revision this module targets, from the [aoeversion] section (blank if absent).
    public string AoeRev { get; set; } = "";

    /// Tokens from the [tags] section, compared case-insensitively (e.g. "civ", "mech", "art", "joke").
    public HashSet<string> Tags { get; set; } = new(System.StringComparer.OrdinalIgnoreCase);
    public string Author { get; set; } = "";
    public List<string> Compatible { get; set; } = new();

    /// Folder names of the modules that must be active and load before this one (from [dependency-hard])
    public List<string> Dependencies { get; set; } = new();

    /// Folder names of modules this one supports but does not require (from [dependency-soft]). They
    /// don't have to be active, but if they are, they should load before this module.
    public List<string> SoftDependencies { get; set; } = new();

    /// Folder names of the modules that must not be active at the same time as this one (from [incompatible]).
    public List<string> Incompatible { get; set; } = new();

    /// Shown as a tooltip when hovering the module row.
    public string ShortDesc { get; set; } = "";

    /// Shown in the popup when the "?" button on the row is clicked.
    public string Desc { get; set; } = "";
}
