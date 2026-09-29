using System.Collections.Generic;

namespace AoELauncher.Models;

/// <summary>
/// Result of checking whether the launcher's own folder is correctly placed
/// as "...\Beyond the Sword\Mods\Ashes of Erebus".
/// </summary>
public class PlacementResult
{
    public string ModPath { get; set; } = "";
    public string? BtsExePath { get; set; }
    public List<string> Errors { get; } = new();
    public bool IsValid => Errors.Count == 0;
}
