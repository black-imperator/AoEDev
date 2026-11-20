using System;
using System.Collections.Generic;
using System.IO;
using System.Text;

namespace AoELauncher.Core;

/// Immediate fix-up of a module's OWN hardcoded paths (`Modules/<Load #>/<ModuleName>/...`) when
/// it is moved to another Load #. What is looked at and rewritten is defined once, in
/// CrossModulePathScanner (`.xml` files under the module's `XML` folder, whole-element paths
/// only), and this uses exactly that code with a lookup that only knows this one module -- so it
/// can never change anything the full scan wouldn't. Other modules' references to the moved
/// module are handled later by the full scan (see MainForm.EnsureCrossModulePaths).
///
/// Also holds the raw-byte file helpers both use: files are processed as bytes so nothing else
/// about them changes (line endings, a UTF-8 BOM, legacy 8-bit encodings); UTF-16 files with a BOM
/// are decoded as such.
public static class ModulePathRewriter
{
    // Latin-1 maps bytes 0-255 to chars 0-255 one-to-one, so decode -> edit -> encode is lossless
    // for any ASCII-compatible encoding (UTF-8, Windows-1252, ISO-8859-1...), which is all that
    // matters since the paths themselves are plain ASCII text around the module name.
    private static readonly Encoding Latin1 = Encoding.GetEncoding(28591);

    /// Rewrites `Modules/<n>/<moduleName>/` to `Modules/<newPass>/<moduleName>/` in the module's
    /// scannable files (moduleDir is the module's folder at its NEW location). Returns one
    /// message per file that couldn't be updated; an empty list means everything went fine.
    public static List<string> Rewrite(string moduleDir, string moduleName, string oldPass, string newPass)
    {
        var errors = new List<string>();
        if (string.Equals(oldPass, newPass, StringComparison.Ordinal)) return errors;

        Func<string, string?> passFor = name =>
            string.Equals(name, moduleName, StringComparison.OrdinalIgnoreCase) ? newPass : null;

        var enumerator = CrossModulePathScanner.EnumerateScannableFiles(moduleDir).GetEnumerator();
        while (true)
        {
            string file;
            try
            {
                if (!enumerator.MoveNext()) break;
                file = enumerator.Current;
            }
            catch (Exception ex)
            {
                errors.Add($"couldn't finish reading the module's XML folder: {ex.Message}");
                break;
            }

            try { CrossModulePathScanner.RewriteFile(file, passFor); }
            catch (Exception ex) { errors.Add($"{CompatHelpers.GetRelativePath(moduleDir, file)}: {ex.Message}"); }
        }

        return errors;
    }

    /// Writes edited text back to a file in the encoding (and BOM) it was read with, temporarily
    /// clearing the read-only attribute if the file has one.
    internal static void WriteEncoded(string file, string text, Encoding encoding, byte[] bom)
    {
        var body = encoding.GetBytes(text);
        var output = new byte[bom.Length + body.Length];
        Buffer.BlockCopy(bom, 0, output, 0, bom.Length);
        Buffer.BlockCopy(body, 0, output, bom.Length, body.Length);

        var attrs = File.GetAttributes(file);
        if ((attrs & FileAttributes.ReadOnly) != 0)
            File.SetAttributes(file, attrs & ~FileAttributes.ReadOnly);
        try { File.WriteAllBytes(file, output); }
        finally
        {
            if ((attrs & FileAttributes.ReadOnly) != 0)
                File.SetAttributes(file, attrs);
        }
    }

    internal static void Decode(byte[] bytes, out string text, out Encoding encoding, out byte[] bom)
    {
        if (bytes.Length >= 2 && bytes[0] == 0xFF && bytes[1] == 0xFE)
        {
            encoding = new UnicodeEncoding(bigEndian: false, byteOrderMark: false);
            bom = new byte[] { 0xFF, 0xFE };
            text = encoding.GetString(bytes, 2, bytes.Length - 2);
        }
        else if (bytes.Length >= 2 && bytes[0] == 0xFE && bytes[1] == 0xFF)
        {
            encoding = new UnicodeEncoding(bigEndian: true, byteOrderMark: false);
            bom = new byte[] { 0xFE, 0xFF };
            text = encoding.GetString(bytes, 2, bytes.Length - 2);
        }
        else
        {
            // Includes a UTF-8 BOM, whose three bytes simply survive as three Latin-1 characters.
            encoding = Latin1;
            bom = Array.Empty<byte>();
            text = Latin1.GetString(bytes);
        }
    }
}
