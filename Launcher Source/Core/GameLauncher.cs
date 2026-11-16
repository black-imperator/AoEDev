using System;
using System.Diagnostics;
using System.IO;

namespace AoELauncher.Core;

public static class GameLauncher
{
    /// Starts Civ4BeyondSword.exe with the given mod folder name enabled,
    /// e.g. modFolderName = "Ashes of Erebus".
    ///
    /// Deliberately uses UseShellExecute = false (a direct Win32
    /// CreateProcess call) rather than true (ShellExecuteEx). A manually
    /// created shortcut with the identical target/arguments launches fine,
    /// but launching the same command line via ShellExecuteEx from this
    /// app produced a process with no window that had to be killed from
    /// Task Manager -- a known class of issue with ShellExecuteEx for game
    /// processes (e.g. Google's Omaha updater changelog lists switching
    /// background process launches from ShellExecute to CreateProcess as a
    /// stability fix for exactly this symptom). CreateProcess is also the
    /// more literal, lower-overhead launch path and is what WorkingDirectory
    /// unambiguously applies to as the new process's actual current
    /// directory (with UseShellExecute = true, WorkingDirectory is instead
    /// documented as just "the location of the executable" for lookup
    /// purposes, which is a subtly different guarantee).
    public static void Launch(string btsExePath, string modFolderName)
    {
        var psi = new ProcessStartInfo
        {
            FileName = btsExePath,
            Arguments = $"mod=\"\\{modFolderName}\"",
            WorkingDirectory = Path.GetDirectoryName(btsExePath) ?? "",
            UseShellExecute = false,
        };
        Process.Start(psi);
    }

    /// True if Civ4BeyondSword.exe is currently running. One quick process-list lookup, meant to be
    /// called when the user interacts with the launcher rather than on a timer. If the process's
    /// path can't be read (e.g. it runs elevated) it still counts as running; a process of the same
    /// name from a different install folder does not.
    public static bool IsRunning(string? btsExePath)
    {
        var processName = Path.GetFileNameWithoutExtension(btsExePath ?? "Civ4BeyondSword.exe");
        Process[] processes;
        try { processes = Process.GetProcessesByName(processName); }
        catch { return false; }

        try
        {
            foreach (var p in processes)
            {
                try
                {
                    var path = p.MainModule?.FileName;
                    if (path == null || btsExePath == null ||
                        string.Equals(Path.GetFullPath(path), Path.GetFullPath(btsExePath), StringComparison.OrdinalIgnoreCase))
                        return true;
                }
                catch { return true; } // access denied / 32-vs-64-bit: it exists, so it's running
            }
            return false;
        }
        finally
        {
            foreach (var p in processes) p.Dispose();
        }
    }
}
