using System;
using System.IO;

namespace AoELauncher.Core;

/// <summary>
/// .NET Framework 4.8 shims for a couple of BCL conveniences the codebase
/// was written against on .NET 8 (<see cref="Convert.ToHexString(byte[])"/>
/// and <see cref="Path.GetRelativePath(string, string)"/>), neither of
/// which exist on .NET Framework. Kept in one place so the call sites that
/// actually care about hashing/paths don't have to carry the workaround
/// logic themselves.
/// </summary>
internal static class CompatHelpers
{
    private static readonly char[] HexChars = "0123456789ABCDEF".ToCharArray();

    /// <summary>Uppercase hex, matching the .NET 5+ Convert.ToHexString default.</summary>
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

    /// <summary>
    /// Classic Uri-based relative-path trick used on .NET Framework before
    /// Path.GetRelativePath existed. Only needs to handle this app's actual
    /// usage (relativeTo is always a directory that's an ancestor of path),
    /// not every edge case of the modern BCL version.
    /// </summary>
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
