using System;
using System.IO;

namespace AoELauncher.Core;

/// .NET Framework 4.8 has neither Convert.ToHexString(byte[]) nor
/// Path.GetRelativePath(string, string); these shims provide them. Kept in
/// one place so the call sites that actually care about hashing/paths don't
/// have to carry the workaround logic themselves.
internal static class CompatHelpers
{
    private static readonly char[] HexChars = "0123456789ABCDEF".ToCharArray();

    /// Uppercase hex, matching the .NET 5+ Convert.ToHexString default.
    public static string ToHexString(byte[] bytes)
    {
        var chars = new char[bytes.Length * 2];
        for (int i = 0; i < bytes.Length; i++)
        {
            chars[i * 2] = HexChars[bytes[i] >> 4];
            chars[i * 2 + 1] = HexChars[bytes[i] & 0xF];
        }
        return new string(chars);
    }

    /// Uri-based relative-path computation. Only needs to handle this app's actual
    /// usage (relativeTo is always a directory that's an ancestor of path),
    /// not every edge case of the modern BCL version.
    public static string GetRelativePath(string relativeTo, string path)
    {
        var fromUri = new Uri(AppendDirectorySeparator(relativeTo));
        var toUri = new Uri(path);

        if (fromUri.Scheme != toUri.Scheme)
            return path;

        var relativeUri = fromUri.MakeRelativeUri(toUri);
        var relativePath = Uri.UnescapeDataString(relativeUri.ToString());

        if (string.Equals(toUri.Scheme, "file", StringComparison.OrdinalIgnoreCase))
            relativePath = relativePath.Replace('/', Path.DirectorySeparatorChar);

        return relativePath;
    }

    private static string AppendDirectorySeparator(string path)
    {
        if (!path.EndsWith(Path.DirectorySeparatorChar.ToString(), StringComparison.Ordinal) &&
            !path.EndsWith(Path.AltDirectorySeparatorChar.ToString(), StringComparison.Ordinal))
            return path + Path.DirectorySeparatorChar;
        return path;
    }
}
