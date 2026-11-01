using System;
using System.IO;
using System.IO.Compression;
using System.Text;
using AoELauncher.Models;

namespace AoELauncher.Core;

/// <summary>
/// Turns a Preset into a compact, pasteable text code (and back again).
///
/// Format: "AoE" + &lt;AshesOfErebus version.txt contents&gt; + ":" + gzip-
/// compressed, base64url-encoded binary payload. The version tag is purely
/// informational (lets the user see what AoE version a code was made
/// against) -- there's only ever one payload format, so there's no
/// multi-version decode logic to maintain.
///
/// Payload (before gzip + base64), a small hand-rolled binary layout rather
/// than JSON, to comfortably fit under Discord's 2000-character message
/// limit even with ~100 modules:
///   byte    : flags. bit 0 (1) = "futureproof" (no version/fingerprint);
///             bit 1 (2) = each module carries a load-pass byte. Codes made before
///             load passes existed have bit 1 clear and still decode fine (their
///             modules just come back with no pass, i.e. "leave where it is").
///   string  : preset name (length-prefixed UTF8)
///   ushort  : module count
///   for each module:
///     string : module folder name (length-prefixed UTF8)
///     [only if bit 1 set:]
///       byte    : load pass (0 = Any, 1-4 = Order\1..4, 255 = unspecified)
///     [only if not futureproof:]
///       string  : version
///       4 bytes : fingerprint (raw bytes, not hex text -- half the size)
/// </summary>
public static class PresetCodec
{
    private const string MagicPrefix = "AoE";

    private const byte FlagFutureproof = 1;
    private const byte FlagHasPass = 2;
    private const byte PassUnspecified = 255;

    private static byte PassToByte(string? pass)
    {
        var p = ModuleLayout.NormalizePass(pass);
        if (p.Length == 0) return PassUnspecified;
        return p == ModuleLayout.AnyPass ? (byte)0 : byte.Parse(p);
    }

    private static string ByteToPass(byte b) =>
        b == 0 ? ModuleLayout.AnyPass : (b >= 1 && b <= 4 ? b.ToString() : "");

    /// <summary>Discord's plain-message character limit, used as the target ceiling for export codes.</summary>
    public const int DiscordSafeLimit = 2000;

    public static string Encode(Preset preset, bool futureproof, string modVersion)
    {
        using var raw = new MemoryStream();
        using (var writer = new BinaryWriter(raw, Encoding.UTF8, leaveOpen: true))
        {
            writer.Write((byte)((futureproof ? FlagFutureproof : 0) | FlagHasPass));
            writer.Write(preset.Name ?? "");
            writer.Write((ushort)preset.Modules.Count);

            foreach (var m in preset.Modules)
            {
                writer.Write(m.Name ?? "");
                writer.Write(PassToByte(m.LoadPass));
                if (!futureproof)
                {
                    writer.Write(m.Version ?? "");
                    writer.Write(FingerprintToBytes(m.Fingerprint));
                }
            }
        }

        using var compressed = new MemoryStream();
        // .NET Framework's CompressionLevel doesn't have SmallestSize (added in .NET 7);
        // Optimal is its closest/best available equivalent there.
        using (var gz = new GZipStream(compressed, CompressionLevel.Optimal, leaveOpen: true))
        {
            var bytes = raw.ToArray();
            gz.Write(bytes, 0, bytes.Length);
        }

        var b64 = Convert.ToBase64String(compressed.ToArray())
            .Replace('+', '-')
            .Replace('/', '_')
            .TrimEnd('=');

        // modVersion (e.g. "379") is free-form text from version.txt; strip any
        // stray ':' just in case, since ':' is the delimiter into the payload.
        var safeVersion = (modVersion ?? "unknown").Replace(":", "");

        return $"{MagicPrefix}{safeVersion}:{b64}";
    }

    public static Preset Decode(string text)
    {
        text = text.Trim();
        if (!text.StartsWith(MagicPrefix, StringComparison.Ordinal))
            throw new FormatException("This doesn't look like a valid Ashes of Erebus preset code.");

        var colonIdx = text.IndexOf(':');
        if (colonIdx < 0 || colonIdx <= MagicPrefix.Length)
            throw new FormatException("This doesn't look like a valid Ashes of Erebus preset code.");

        var sourceVersion = text.Substring(MagicPrefix.Length, colonIdx - MagicPrefix.Length);
        var b64 = text.Substring(colonIdx + 1).Replace('-', '+').Replace('_', '/');
        switch (b64.Length % 4)
        {
            case 2: b64 += "=="; break;
            case 3: b64 += "="; break;
        }

        byte[] compressed;
        try
        {
            compressed = Convert.FromBase64String(b64);
        }
        catch (FormatException)
        {
            throw new FormatException("The preset code appears to be corrupted or incomplete.");
        }

        byte[] raw;
        try
        {
            using var msIn = new MemoryStream(compressed);
            using var gz = new GZipStream(msIn, CompressionMode.Decompress);
            using var msOut = new MemoryStream();
            gz.CopyTo(msOut);
            raw = msOut.ToArray();
        }
        catch (InvalidDataException)
        {
            throw new FormatException("The preset code appears to be corrupted or incomplete.");
        }

        try
        {
            using var msRead = new MemoryStream(raw);
            using var reader = new BinaryReader(msRead, Encoding.UTF8);

            var preset = new Preset { SourceVersion = sourceVersion };
            var flags = reader.ReadByte();
            bool futureproof = (flags & FlagFutureproof) != 0;
            bool hasPass = (flags & FlagHasPass) != 0;
            preset.Name = reader.ReadString();
            var count = reader.ReadUInt16();

            for (int i = 0; i < count; i++)
            {
                var mod = new ModuleRef { Name = reader.ReadString() };
                if (hasPass) mod.LoadPass = ByteToPass(reader.ReadByte());
                if (!futureproof)
                {
                    mod.Version = reader.ReadString();
                    mod.Fingerprint = BytesToFingerprint(reader.ReadBytes(4));
                }
                preset.Modules.Add(mod);
            }

            return preset;
        }
        catch (EndOfStreamException)
        {
            throw new FormatException("The preset code appears to be corrupted or incomplete.");
        }
    }

    private static byte[] FingerprintToBytes(string fingerprintHex)
    {
        // ModuleScanner.ComputeFingerprint always returns 8 hex chars (4 bytes).
        if (string.IsNullOrEmpty(fingerprintHex))
            return new byte[4];

        // No System.Range on .NET Framework -- fingerprintHex[..8] won't compile there.
        var hex = fingerprintHex.Length >= 8 ? fingerprintHex.Substring(0, 8) : fingerprintHex.PadRight(8, '0');
        var bytes = new byte[4];
        for (int i = 0; i < 4; i++)
            bytes[i] = Convert.ToByte(hex.Substring(i * 2, 2), 16);
        return bytes;
    }

    private static string BytesToFingerprint(byte[] bytes) => CompatHelpers.ToHexString(bytes);
}
