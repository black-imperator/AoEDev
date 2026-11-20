using System;
using System.Collections.Concurrent;
using System.Collections.Generic;
using System.IO;
using System.Linq;
using System.Text.RegularExpressions;
using System.Threading;
using System.Threading.Tasks;

namespace AoELauncher.Core;

/// Modules hardcode paths to module folders (`Modules/<Load #>/<Module>/...`) -- their own, and
/// sometimes another module's, without necessarily declaring a dependency. When a module changes
/// Load #, every such path pointing at it has to follow.
///
/// This class holds the ONE definition of what gets looked at and what gets rewritten, shared by
/// the full scan (Run) and by the immediate self-rewrite when a module is moved
/// (ModulePathRewriter.Rewrite), so neither can ever find something the other wouldn't:
///  - only `.xml` files under `<Module>/XML/` (never `*Schema.xml`, never Art or anything else);
///  - only elements whose whole content is a path starting with `Modules` (`>Modules/N/Name/...<`);
///  - references to modules that aren't installed are left alone.
/// Files are edited as raw bytes (see ModulePathRewriter.Decode) so encoding, BOM and line
/// endings survive, and are only rewritten if something actually changed.
public static class CrossModulePathScanner
{
    public sealed class ScanResult
    {
        public int FilesScanned;
        public int FilesChanged;
        public int ReferencesUpdated;
        public List<string> Errors { get; } = new();

        /// ACTIVE modules that contain a path into a module that is only installed INACTIVE (so the
        /// game can't find it there). Usually a dependency the author forgot to declare. Each pair
        /// is listed once, as folder names; self-references never count.
        public List<InactiveReference> InactiveReferences { get; } = new();
    }

    public sealed class InactiveReference
    {
        public string FromModule { get; set; } = "";
        public string ToModule { get; set; } = "";
    }

    /// The folder inside a module that is searched.
    public const string XmlFolderName = "XML";

    private const long MaxFileBytes = 64L * 1024 * 1024;

    // `>` + optional whitespace + Modules<sep><pass><sep><ModuleFolder> where the rest of the element
    // is more path (a separator then anything up to the next tag). Either slash direction.
    private static readonly Regex PathPattern = new(
        @"(?<=>)(\s*Modules[\\/]+)(\d+)([\\/]+)([^\\/<>\r\n]+)(?=[\\/][^<>]*<)",
        RegexOptions.IgnoreCase | RegexOptions.CultureInvariant | RegexOptions.Compiled);

    /// Every file of a module that the scan looks at: `.xml` files anywhere under `<module>/XML`,
    /// except `*Schema.xml`.
    public static IEnumerable<string> EnumerateScannableFiles(string moduleDir)
    {
        var xmlDir = Path.Combine(moduleDir, XmlFolderName);
        if (!Directory.Exists(xmlDir)) yield break;

        foreach (var file in Directory.EnumerateFiles(xmlDir, "*.xml", SearchOption.AllDirectories))
        {
            // The "*.xml" search pattern can also match longer extensions on .NET Framework.
            if (!string.Equals(Path.GetExtension(file), ".xml", StringComparison.OrdinalIgnoreCase)) continue;
            if (file.EndsWith("Schema.xml", StringComparison.OrdinalIgnoreCase)) continue;
            yield return file;
        }
    }

    /// True if `file` (inside `moduleDir`) is one the scan would look at.
    public static bool IsScannable(string moduleDir, string file)
    {
        if (!string.Equals(Path.GetExtension(file), ".xml", StringComparison.OrdinalIgnoreCase)) return false;
        if (file.EndsWith("Schema.xml", StringComparison.OrdinalIgnoreCase)) return false;
        var rel = CompatHelpers.GetRelativePath(moduleDir, file);
        var top = rel.Split(Path.DirectorySeparatorChar, Path.AltDirectorySeparatorChar)[0];
        return top.Equals(XmlFolderName, StringComparison.OrdinalIgnoreCase);
    }

    /// Rewrites one file: every matching path whose module `passFor` knows (returns its current
    /// Load #, or null for "leave alone") and whose number is different gets the right number.
    /// `onReference`, if given, is told the folder name of every known module a path points at
    /// (whether or not it needed changing). Returns how many paths were changed (the file is only
    /// written if that is above zero). Throws on I/O problems.
    public static int RewriteFile(string file, Func<string, string?> passFor, Action<string>? onReference = null)
    {
        var info = new FileInfo(file);
        if (info.Length == 0 || info.Length > MaxFileBytes) return 0;

        var bytes = File.ReadAllBytes(file);
        ModulePathRewriter.Decode(bytes, out var text, out var encoding, out var bom);
        if (text.IndexOf("Modules", StringComparison.OrdinalIgnoreCase) < 0) return 0;

        int hits = 0;
        var rewritten = PathPattern.Replace(text, m =>
        {
            var actual = passFor(m.Groups[4].Value);
            if (actual == null) return m.Value; // not a module we know about
            onReference?.Invoke(m.Groups[4].Value);
            if (string.Equals(m.Groups[2].Value, actual, StringComparison.Ordinal)) return m.Value; // already right
            hits++;
            return m.Groups[1].Value + actual + m.Groups[3].Value + m.Groups[4].Value;
        });
        if (hits == 0) return 0;

        ModulePathRewriter.WriteEncoded(file, rewritten, encoding, bom);
        return hits;
    }

    /// The file's bytes with the Load # of the module's OWN paths blanked to "#" (same matching
    /// rules as the rewrite), so a fingerprint doesn't change just because the module sits in a
    /// different Load # folder.
    public static byte[] NormalizeForFingerprint(byte[] bytes, string moduleName)
    {
        ModulePathRewriter.Decode(bytes, out var text, out var encoding, out var bom);
        if (text.IndexOf("Modules", StringComparison.OrdinalIgnoreCase) < 0) return bytes;

        var updated = PathPattern.Replace(text, m =>
            string.Equals(m.Groups[4].Value, moduleName, StringComparison.OrdinalIgnoreCase)
                ? m.Groups[1].Value + "#" + m.Groups[3].Value + m.Groups[4].Value
                : m.Value);
        if (updated == text) return bytes;

        var body = encoding.GetBytes(updated);
        var output = new byte[bom.Length + body.Length];
        Buffer.BlockCopy(bom, 0, output, 0, bom.Length);
        Buffer.BlockCopy(body, 0, output, bom.Length, body.Length);
        return output;
    }

    /// The full scan: every installed module (active and inactive), every scannable file.
    /// `progress`, if given, is called (on the calling thread) as each phase starts, so a caller can
    /// show where a slow scan is.
    public static ScanResult Run(string modPath, Action<string>? progress = null)
    {
        var result = new ScanResult();
        progress?.Invoke("Checking module file paths: listing modules...");

        // Folder name -> Load #. Active modules win over an inactive copy of the same name.
        var passByName = new Dictionary<string, string>(StringComparer.OrdinalIgnoreCase);
        var activeNames = new HashSet<string>(StringComparer.OrdinalIgnoreCase);
        var roots = new List<(string Dir, bool Active)>();
        foreach (var active in new[] { true, false })
        {
            foreach (var pass in ModuleLayout.Passes)
            {
                var dir = ModuleLayout.GetPassDir(modPath, active, pass);
                if (!Directory.Exists(dir)) continue;
                string[] subs;
                try { subs = Directory.GetDirectories(dir); }
                catch (Exception ex) { result.Errors.Add($"{dir}: {ex.Message}"); continue; }

                foreach (var sub in subs)
                {
                    var name = Path.GetFileName(sub);
                    if (!passByName.ContainsKey(name)) passByName[name] = pass;
                    if (active) activeNames.Add(name);
                    roots.Add((sub, active));
                }
            }
        }

        progress?.Invoke($"Checking module file paths: listing XML files in {roots.Count} modules...");
        var files = new List<(string File, string Module, bool Active)>();
        foreach (var (dir, active) in roots)
        {
            var module = Path.GetFileName(dir);
            try { files.AddRange(EnumerateScannableFiles(dir).Select(f => (f, module, active))); }
            catch (Exception ex)
            {
                result.Errors.Add($"{module}: couldn't read the module's XML folder: {ex.Message}");
            }
        }
        progress?.Invoke($"Checking module file paths: reading {files.Count} XML files...");

        var errors = new ConcurrentBag<string>();
        int scanned = 0, changed = 0, updated = 0;
        Func<string, string?> passFor = name => passByName.TryGetValue(name, out var p) ? p : null;

        var inactiveRefs = new ConcurrentDictionary<(string From, string To), byte>();

        Parallel.ForEach(files, new ParallelOptions { MaxDegreeOfParallelism = Math.Max(1, Environment.ProcessorCount - 1) }, item =>
        {
            try
            {
                Interlocked.Increment(ref scanned);

                Action<string>? onReference = null;
                if (item.Active)
                {
                    onReference = target =>
                    {
                        if (!string.Equals(target, item.Module, StringComparison.OrdinalIgnoreCase) && !activeNames.Contains(target))
                            inactiveRefs.TryAdd((item.Module, target), 0);
                    };
                }

                var hits = RewriteFile(item.File, passFor, onReference);
                if (hits == 0) return;
                Interlocked.Increment(ref changed);
                Interlocked.Add(ref updated, hits);
            }
            catch (Exception ex)
            {
                errors.Add($"{CompatHelpers.GetRelativePath(modPath, item.File)}: {ex.Message}");
            }
        });

        result.FilesScanned = scanned;
        result.FilesChanged = changed;
        result.ReferencesUpdated = updated;
        result.Errors.AddRange(errors);
        foreach (var pair in inactiveRefs.Keys.OrderBy(k => k.From, StringComparer.OrdinalIgnoreCase).ThenBy(k => k.To, StringComparer.OrdinalIgnoreCase))
            result.InactiveReferences.Add(new InactiveReference { FromModule = pair.From, ToModule = pair.To });
        return result;
    }
}
