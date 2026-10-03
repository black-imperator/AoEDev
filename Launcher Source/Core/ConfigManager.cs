using System;
using System.IO;
using System.Xml.Serialization;
using AoELauncher.Models;

namespace AoELauncher.Core;

/// <summary>
/// Reads/writes the single config+save file that always lives right next to
/// the exe. There is intentionally no fallback location (such as
/// %LocalAppData%): the launcher ships as part of the Ashes of Erebus
/// folder, so its own directory is always where the config belongs. If that
/// location isn't writable, Save() throws and the caller is expected to
/// show the user a clear error rather than silently writing somewhere else.
///
/// XML rather than JSON: this targets .NET Framework 4.8 (framework-
/// dependent, no bundled runtime, so the exe stays under 1MB), and
/// System.Text.Json isn't part of the Framework's own BCL -- pulling it in
/// as a NuGet package would mean shipping extra DLLs alongside the exe just
/// for this one file. XmlSerializer is built into .NET Framework with no
/// extra dependencies, so it's the simpler fit here.
/// </summary>
public static class ConfigManager
{
    private const string FileName = "aoe_launcher_config.xml";

    private static readonly XmlSerializer Serializer = new(typeof(AppConfig));

    public static string ConfigPath { get; } = Path.Combine(AppContext.BaseDirectory, FileName);

    public static AppConfig Load()
    {
        if (!File.Exists(ConfigPath))
            return new AppConfig();

        try
        {
            using var stream = File.OpenRead(ConfigPath);
            return (AppConfig?)Serializer.Deserialize(stream) ?? new AppConfig();
        }
        catch
        {
            // Corrupt or unreadable config: don't crash the app, just start fresh.
            return new AppConfig();
        }
    }

    /// <summary>Throws if the file can't be written (e.g. read-only location); callers should catch and inform the user.</summary>
    public static void Save(AppConfig config)
    {
        using var stream = File.Create(ConfigPath);
        Serializer.Serialize(stream, config);
    }
}
