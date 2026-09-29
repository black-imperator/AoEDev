using System;
using System.Collections.Generic;
using System.IO;
using System.Linq;
using AoELauncher.Models;

namespace AoELauncher.Core;

/// <summary>
/// Implements the "Update Schemas" action: every file under a module's
/// "XML" subfolder whose name ends in "Schema.xml" is compared against the
/// corresponding schema file in Ashes of Erebus's own base XML (NOT the
/// base game's) and, if the contents differ, gets overwritten to match.
/// Files that are already byte-for-byte identical are skipped entirely --
/// not counted, not reported -- so the preview and result only ever show
/// modules/files that actually have something to change.
///
/// Split into Plan() (a dry run that touches no files, for showing the
/// user a "here's what will happen" confirmation) and Apply() (performs
/// the actual copies from a previously computed plan).
///
/// Matching rule: given a module file name like "Dao_CIV4TerrainSchema.xml"
/// (or "D_CIV4TerrainSchema.xml", etc.), the parent schema's file name is
/// everything after the LAST underscore -- stock schema file names never
/// contain an underscore, but a module's own prefix sometimes does, so
/// splitting on the last one is the reliable choice. A file with no
/// underscore at all is assumed to already be the plain schema name.
///
/// Folder structure mirrors between module and the mod's base XML: a file at
///   &lt;module&gt;\XML\&lt;subpath&gt;\&lt;file&gt;
/// (subpath may be empty, i.e. the file can sit directly under XML\) maps to
///   &lt;Ashes of Erebus&gt;\Assets\XML\&lt;subpath&gt;\&lt;parentFileName&gt;
/// </summary>
public static class SchemaUpdater
{
    public static SchemaUpdatePlan Plan(string modPath, IEnumerable<ModuleInfo> allModules)
    {
        var plan = new SchemaUpdatePlan();
        var baseXmlDir = Path.Combine(modPath, "Assets", "XML");

        foreach (var module in allModules)
        {
            var moduleXmlDir = Path.Combine(module.FullPath, "XML");
            if (!Directory.Exists(moduleXmlDir)) continue;

            var report = new ModuleSchemaReport { ModuleName = module.Name };

            foreach (var file in Directory.EnumerateFiles(moduleXmlDir, "*Schema.xml", SearchOption.AllDirectories))
            {
                var fileName = Path.GetFileName(file);
                var relDir = Path.GetDirectoryName(CompatHelpers.GetRelativePath(moduleXmlDir, file)) ?? "";

                var underscoreIdx = fileName.LastIndexOf('_');
                // No System.Range on .NET Framework -- fileName[(underscoreIdx + 1)..] won't compile there.
                var parentFileName = underscoreIdx >= 0 ? fileName.Substring(underscoreIdx + 1) : fileName;

                var sourcePath = string.IsNullOrEmpty(relDir)
                    ? Path.Combine(baseXmlDir, parentFileName)
                    : Path.Combine(baseXmlDir, relDir, parentFileName);

                if (!File.Exists(sourcePath))
                {
                    report.Errors.Add(
                        $"{fileName}: no matching base schema found (looked for " +
                        $"{CompatHelpers.GetRelativePath(modPath, sourcePath)})");
                    continue;
                }

                if (FilesAreIdentical(sourcePath, file))
                    continue; // no delta -- nothing to report or update

                plan.Updates.Add(new PlannedFileUpdate
                {
                    ModuleName = module.Name,
                    FileName = fileName,
                    DestPath = file,
                    SourcePath = sourcePath,
                });
                report.UpdatedCount++;
            }

            if (report.UpdatedCount > 0 || report.Errors.Count > 0)
                plan.ModuleReports.Add(report);
        }

        return plan;
    }

    public static SchemaApplyResult Apply(SchemaUpdatePlan plan)
    {
        var result = new SchemaApplyResult();
        var errorsByModule = new Dictionary<string, List<string>>(StringComparer.OrdinalIgnoreCase);

        foreach (var update in plan.Updates)
        {
            try
            {
                File.Copy(update.SourcePath, update.DestPath, overwrite: true);
                result.TotalUpdated++;
            }
            catch (Exception ex)
            {
                result.TotalErrors++;
                if (!errorsByModule.TryGetValue(update.ModuleName, out var list))
                    errorsByModule[update.ModuleName] = list = new List<string>();
                list.Add($"{update.FileName}: {ex.Message}");
            }
        }

        foreach (var kvp in errorsByModule)
            result.ErrorReports.Add(new ModuleSchemaReport { ModuleName = kvp.Key, Errors = kvp.Value });

        return result;
    }

    private static bool FilesAreIdentical(string pathA, string pathB)
    {
        var infoA = new FileInfo(pathA);
        var infoB = new FileInfo(pathB);
        if (infoA.Length != infoB.Length) return false;

        var bytesA = File.ReadAllBytes(pathA);
        var bytesB = File.ReadAllBytes(pathB);
        // AsSpan()-based comparison needs System.Memory; a plain LINQ
        // SequenceEqual (already using System.Linq here) avoids that dependency.
        return bytesA.SequenceEqual(bytesB);
    }
}

public class SchemaUpdatePlan
{
    public List<PlannedFileUpdate> Updates { get; } = new();
    public List<ModuleSchemaReport> ModuleReports { get; } = new();
    public int TotalPlannedUpdates => Updates.Count;
    public int TotalErrors => ModuleReports.Sum(r => r.Errors.Count);
}

public class PlannedFileUpdate
{
    public string ModuleName { get; set; } = "";
    public string FileName { get; set; } = "";
    public string DestPath { get; set; } = "";
    public string SourcePath { get; set; } = "";
}

public class ModuleSchemaReport
{
    public string ModuleName { get; set; } = "";
    public int UpdatedCount;
    public List<string> Errors { get; set; } = new();
}

public class SchemaApplyResult
{
    public int TotalUpdated;
    public int TotalErrors;
    public List<ModuleSchemaReport> ErrorReports { get; } = new();
}
