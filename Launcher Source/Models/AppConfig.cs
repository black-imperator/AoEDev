using System.Collections.Generic;

namespace AoELauncher.Models;

/// A single module as recorded inside a preset (not a live scan result).
public class ModuleRef
{
    public string Name { get; set; } = "";

    /// Empty when exported in "futureproof" mode.
    public string Version { get; set; } = "";

    /// 8-hex-char fingerprint (see ModuleScanner.ComputeFingerprint). Empty
    /// when exported in "futureproof" mode, in which case no change
    /// detection is possible or attempted for this module on import.
    public string Fingerprint { get; set; } = "";

    /// The load pass the module was in when the preset was saved: "Def", "1".."4", or empty if
    /// unspecified. Empty means "leave the module in whatever pass it's currently in" when the
    /// preset is applied.
    public string LoadPass { get; set; } = "";
}

public class Preset
{
    public string Name { get; set; } = "";
    public List<ModuleRef> Modules { get; set; } = new();

    /// The Ashes of Erebus version (from version.txt) this preset was
    /// exported against, e.g. "379". Set locally when saving, and parsed
    /// out of the share code's "AoE[ver]:" prefix when importing. Purely
    /// informational -- never blocks an import, just lets the user know if
    /// they're applying a preset made against a different AoE version.
    public string SourceVersion { get; set; } = "";
}

/// The single file this app persists to disk: the saved presets and the
/// launcher's user settings (close-on-launch, modules panel visibility, window size).
/// There's no override/location data here -- the mod folder is always
/// wherever this exe is running from, and Civ4BeyondSword.exe is always
/// found relative to that (see InstallLocator); if placement is wrong the
/// user needs to fix the placement, not configure around it.
public class AppConfig
{
    public List<Preset> Presets { get; set; } = new();

    /// If true, the launcher quits itself right after successfully starting the game.
    public bool CloseOnLaunch { get; set; }

    /// Whether the module lists and preset tools are shown (the "Manage Modules" / "Hide Modules"
    /// toggle). Defaults to hidden.
    public bool ModulesVisible { get; set; }

    /// Window client-area width in pixels when not maximized; 0 means "use the default size".
    public int WindowClientWidth { get; set; }

    /// Window client-area height in pixels while the module section is shown (the hidden state has
    /// a fixed height, so only the expanded height is worth remembering); 0 means "use the default".
    public int WindowClientHeight { get; set; }

    /// Whether the window was maximized (only possible while the module section is shown).
    public bool WindowMaximized { get; set; }
}
