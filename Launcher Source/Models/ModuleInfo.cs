using System.Collections.Generic;

namespace AoELauncher.Models;

/// <summary>
/// Represents a module folder as currently found on disk (either active or
/// inactive), including everything parsed out of its info.txt.
/// </summary>
public class ModuleInfo
{
    public string Name { get; set; } = "";
    public string FullPath { get; set; } = "";
    public bool IsActive { get; set; }

    /// <summary>"Any" if stored under Any\, otherwise "1".."4" for Order\1..4 (see Core/ModuleLayout).</summary>
    public string LoadPass { get; set; } = "Any";

    // --- from info.txt ---
    public string Version { get; set; } = "unknown";

    /// <summary>The Ashes of Erebus revision this module targets, from the [aoeversion] section (blank if absent).</summary>
    public string AoeRev { get; set; } = "";

    /// <summary>Tokens from the [tags] section, compared case-insensitively (e.g. "civ", "mech", "art", "joke").</summary>
    public HashSet<string> Tags { get; set; } = new(System.StringComparer.OrdinalIgnoreCase);
    public string RifeVersion { get; set; } = "";
    public string Author { get; set; } = "";
    public List<string> Compatible { get; set; } = new();

    /// <summary>Shown as a tooltip when hovering the module row.</summary>
    public string ShortDesc { get; set; } = "";

    /// <summary>Shown in the popup when the "?" button on the row is clicked.</summary>
    public string Desc { get; set; } = "";
}
