using System;
using System.Collections.Generic;
using System.IO;
using System.Linq;
using System.Security.Cryptography;
using System.Text;
using System.Text.RegularExpressions;
using AoELauncher.Models;

namespace AoELauncher.Core;

public static class ModuleScanner
{
    private static readonly Regex SectionHeader = new(@"^\[(\w+)\]$", RegexOptions.Compiled);

    /// <summary>
    /// Scans both the active and inactive NormalModules folders and returns
    /// every module found, with everything parsed out of its info.txt.
    /// </summary>
    public static List<ModuleInfo> ScanAll(string modPath)
    {
        var list = new List<ModuleInfo>();
        list.AddRange(ScanDirectory(Path.Combine(modPath, "Assets", "Modules", "NormalModules"), isActive: true));
        list.AddRange(ScanDirectory(Path.Combine(modPath, "Assets", "Inactive Modules", "NormalModules"), isActive: false));
        return list;
    }

    private static List<ModuleInfo> ScanDirectory(string dir, bool isActive)
    {
        var result = new List<ModuleInfo>();
        if (!Directory.Exists(dir)) return result;

        foreach (var sub in Directory.GetDirectories(dir))
        {
            var info = ReadInfo(sub);
            info.Name = Path.GetFileName(sub);
            info.FullPath = sub;
            info.IsActive = isActive;
            result.Add(info);
        }

        return result;
    }

    /// <summary>
    /// Parses AoE's info.txt format:
    ///   ;comment lines starting with a semicolon are ignored
    ///   [section]
    ///   value line(s) until the next [section] or end of file
    /// [desc] may be multi-line (including blank lines for paragraph breaks);
    /// everything else is treated as a single line.
    /// </summary>
    private static ModuleInfo ReadInfo(string moduleDir)
    {
        var info = new ModuleInfo();
        var infoFile = Path.Combine(moduleDir, "info.txt");
        if (!File.Exists(infoFile))
        {
            info.Version = "unknown";
            return info;
        }

        try
        {
            string? currentSection = null;
            var buffer = new List<string>();

            void Flush()
            {
                if (currentSection == null) return;
                var text = string.Join("\n", buffer).Trim();

                switch (currentSection)
                {
                    case "version": info.Version = FirstLine(text); break;
                    case "rifeversion": info.RifeVersion = FirstLine(text); break;
                    case "author": info.Author = FirstLine(text); break;
                    case "shortdesc": info.ShortDesc = FirstLine(text); break;
                    case "desc": info.Desc = text; break;
                    case "compatible":
                        // .NET Framework has no Split(char, StringSplitOptions) overload or
                        // TrimEntries option, so split on an array and trim manually.
                        info.Compatible = text
                            .Split(new[] { '\n' }, StringSplitOptions.RemoveEmptyEntries)
                            .Select(s => s.Trim())
                            .Where(s => s.Length > 0)
                            .ToList();
                        break;
                    // "name" is intentionally not used to override the folder name --
                    // the folder name is what the file system (and drag/drop) actually operates on.
                }
            }

            foreach (var rawLine in File.ReadAllLines(infoFile))
            {
                var line = rawLine.TrimEnd();
                var trimmedStart = line.TrimStart();

                if (trimmedStart.StartsWith(";", StringComparison.Ordinal))
                    continue; // comment line, ignore entirely

                var m = SectionHeader.Match(trimmedStart);
                if (m.Success)
                {
                    Flush();
                    currentSection = m.Groups[1].Value.ToLowerInvariant();
                    buffer.Clear();
                    continue;
                }

                buffer.Add(line);
            }
            Flush();
        }
        catch
        {
            // Unreadable info.txt: fall back to defaults below.
        }

        if (string.IsNullOrWhiteSpace(info.Version)) info.Version = "unknown";
        return info;
    }

    private static string FirstLine(string text)
    {
        var idx = text.IndexOf('\n');
        // .NET Framework has no System.Range/System.Index types, so the C# 8
        // range operator (text[..idx]) won't compile there -- use Substring instead.
        var s = idx >= 0 ? text.Substring(0, idx) : text;
        return s.Trim();
    }

    /// <summary>
    /// Computes a fingerprint of a module folder's contents, returned as an
    /// 8-character hex string (32 bits). This is a "did this module change"
    /// signal, not a security hash, and is tuned for how AoE modules are
    /// actually structured:
    ///   - Files ending in "Schema.xml" are skipped entirely (not even
    ///     checked by path/size). These are refreshed independently by the
    ///     "Update Schemas" action from the base game's own XML, and can
    ///     legitimately change without the module itself being updated, so
    ///     including them here would produce constant false-positive
    ///     "this module changed" warnings.
    ///   - Files under a top-level "Art" folder are large binary assets;
    ///     checked only by relative path + file size, never content, since
    ///     hashing gigabytes of textures on every export would be far too
    ///     slow.
    ///   - Everything else (XML/txt gameplay data, small and numerous) gets
    ///     a full SHA-256 content hash, since a single changed value in one
    ///     of these files can cause multiplayer desyncs and deserves exact
    ///     detection.
    ///   - Last-write timestamps are never used: they don't reliably
    ///     indicate an actual content change and would produce false
    ///     positives (e.g. after a re-extract).
    /// </summary>
    public static string ComputeFingerprint(string moduleDir)
    {
        try
        {
            var entries = new List<string>();

            foreach (var file in Directory.EnumerateFiles(moduleDir, "*", SearchOption.AllDirectories))
            {
                if (file.EndsWith("Schema.xml", StringComparison.OrdinalIgnoreCase))
                    continue;

                var rel = CompatHelpers.GetRelativePath(moduleDir, file);
                var topSegment = rel.Split(Path.DirectorySeparatorChar, Path.AltDirectorySeparatorChar)[0];
                bool isArt = topSegment.Equals("Art", StringComparison.OrdinalIgnoreCase);

                if (isArt)
                {
                    var fi = new FileInfo(file);
                    entries.Add($"{rel}|{fi.Length}");
                }
                else
                {
                    // SHA256.HashData(Stream/byte[]) is a .NET 5+ static convenience;
                    // .NET Framework needs an instance via SHA256.Create().
                    using var sha256 = SHA256.Create();
                    using var stream = File.OpenRead(file);
                    var hash = sha256.ComputeHash(stream);
                    entries.Add($"{rel}|{CompatHelpers.ToHexString(hash)}");
                }
            }

            entries.Sort(StringComparer.Ordinal);
            var joined = string.Join("\n", entries);
            byte[] combined;
            using (var sha256 = SHA256.Create())
                combined = sha256.ComputeHash(Encoding.UTF8.GetBytes(joined));
            return CompatHelpers.ToHexString(combined).Substring(0, 8);
        }
        catch
        {
            return "";
        }
    }
}
