using System;
using System.IO;
using AoELauncher.Models;

namespace AoELauncher.Core;

/// <summary>
/// Confirms the launcher (and therefore the Ashes of Erebus folder it ships
/// inside) is placed correctly, without touching the registry or scanning
/// the disk for Steam/GOG installs. Since the launcher exe is distributed as
/// part of the mod itself, its own folder location tells us everything we
/// need: it should be named exactly "Ashes of Erebus", sitting directly
/// inside a folder named "Mods", which itself sits directly inside the
/// Beyond the Sword folder (the one containing Civ4BeyondSword.exe).
///
/// The classic first-time mistake on Steam is placing the mod folder at
///   ...\Sid Meier's Civilization IV Beyond the Sword\Mods\Ashes of Erebus
/// instead of
///   ...\Sid Meier's Civilization IV Beyond the Sword\Beyond the Sword\Mods\Ashes of Erebus
/// Checking for Civ4BeyondSword.exe two levels up catches exactly this.
/// </summary>
public static class InstallLocator
{
    public const string ExpectedFolderName = "Ashes of Erebus";
    public const string ModsFolderName = "Mods";
    public const string BtsExeName = "Civ4BeyondSword.exe";

    public static PlacementResult ValidatePlacement(string modPath)
    {
        var result = new PlacementResult { ModPath = modPath };

        if (!Directory.Exists(modPath))
        {
            result.Errors.Add("The launcher's own folder doesn't seem to exist. This shouldn't normally happen.");
            return result;
        }

        var folderName = Path.GetFileName(modPath.TrimEnd(Path.DirectorySeparatorChar, Path.AltDirectorySeparatorChar));
        if (!string.Equals(folderName, ExpectedFolderName, StringComparison.Ordinal))
        {
            result.Errors.Add(
                $"This folder is named \"{folderName}\", but it needs to be named exactly \"{ExpectedFolderName}\". " +
                "Renaming the mod folder is known to cause other problems -- please rename it back and re-check.");
        }

        var modsDir = Directory.GetParent(modPath);
        if (modsDir == null || !string.Equals(modsDir.Name, ModsFolderName, StringComparison.OrdinalIgnoreCase))
        {
            result.Errors.Add(
                $"This folder's parent should be named \"{ModsFolderName}\", but found " +
                $"\"{(modsDir?.Name ?? "(nothing -- this folder has no parent)")}\" instead.");
        }

        var btsDir = modsDir?.Parent;
        string? exePath = null;
        if (btsDir != null)
        {
            var candidateExe = Path.Combine(btsDir.FullName, BtsExeName);
            if (File.Exists(candidateExe))
                exePath = candidateExe;
        }

        if (exePath == null)
        {
            var btsDirDisplay = btsDir?.FullName ?? "(unknown -- couldn't walk up two levels)";
            result.Errors.Add(
                $"Couldn't find {BtsExeName} in the folder two levels up ({btsDirDisplay}). " +
                "This is usually because the mod folder is nested one level too shallow -- for a Steam install it " +
                "should be at\n\"...Sid Meier's Civilization IV Beyond the Sword\\Beyond the Sword\\Mods\\Ashes of Erebus\",\n" +
                "not\n\"...Sid Meier's Civilization IV Beyond the Sword\\Mods\\Ashes of Erebus\".");
        }
        result.BtsExePath = exePath;

        var activeDir = Path.Combine(modPath, "Assets", "Modules", "NormalModules");
        var inactiveDir = Path.Combine(modPath, "Assets", "Inactive Modules", "NormalModules");
        if (!Directory.Exists(activeDir) && !Directory.Exists(inactiveDir))
        {
            result.Errors.Add(
                "This doesn't look like an Ashes of Erebus install -- missing " +
                "Assets\\Modules\\NormalModules and Assets\\Inactive Modules\\NormalModules.");
        }
        else
        {
            try
            {
                Directory.CreateDirectory(activeDir);
                Directory.CreateDirectory(inactiveDir);
            }
            catch (Exception ex)
            {
                result.Errors.Add($"Couldn't prepare the module folders: {ex.Message}");
            }
        }

        return result;
    }
}
