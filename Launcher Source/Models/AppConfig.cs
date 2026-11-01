using System.Collections.Generic;

namespace AoELauncher.Models;

/// <summary>
/// A single module as recorded inside a preset (not a live scan result).
/// </summary>
public class ModuleRef
{
    public string Name { get; set; } = "";

    /// <summary>Empty when exported in "futureproof" mode.</summary>
    public string Version { get; set; } = "";

    /// <summary>
    /// 8-hex-char fingerprint (see ModuleScanner.ComputeFingerprint). Empty
    /// when exported in "futureproof" mode, in which case no change
    /// detection is possible or attempted for this module on import.
    /// </summary>
    public string Fingerprint { get; set; } = "";

    /// <summary>
    /// The load pass the module was in when the preset was saved: "Any", "1".."4", or empty if
    /// unknown (presets saved/exported before load passes existed). Empty means "leave the module
    /// in whatever pass it's currently in" when the preset is applied.
    /// </summary>
    public string LoadPass { get; set; } = "";
}

public class Preset
{
    public string Name { get; set; } = "";
    public List<ModuleRef> Modules { get; set; } = new();

    /// <summary>
    /// The Ashes of Erebus version (from version.txt) this preset was
    /// exported against, e.g. "379". Set locally when saving, and parsed
    /// out of the share code's "AoE[ver]:" prefix when importing. Purely
    /// informational -- never blocks an import, just lets the user know if
    /// they're applying a preset made against a different AoE version.
    /// </summary>
    public string SourceVersion { get; set; } = "";
}

/// <summary>
/// The single file this app persists to disk: the saved presets and the
/// launcher's user settings (close-on-launch, modules panel visibility).
/// There's no override/location data here -- the mod folder is always
/// wherever this exe is running from, and Civ4BeyondSword.exe is always
/// found relative to that (see InstallLocator); if placement is wrong the
/// user needs to fix the placement, not configure around it.
/// </summary>
public class AppConfig
{
    public List<Preset> Presets { get; set; } = new();

    /// <summary>If true, the launcher quits itself right after successfully starting the game.</summary>
    public bool CloseOnLaunch { get; set; }

    /// <summary>
    /// Whether the module lists and preset tools are shown (the "Manage Modules" / "Hide Modules"
    /// toggle). Defaults to hidden, which is also what a config file from an older version gets.
    /// </summary>
    public bool ModulesVisible { get; set; }
}
