# Ashes of Erebus Launcher

A lightweight, standalone module manager and launcher for the Civilization IV mod
*Ashes of Erebus*. Ships as a single small `.exe` (targets .NET Framework 4.8,
framework-dependent -- not self-contained, so it stays well under 1MB and relies
on the .NET Framework already present on the machine rather than bundling a
runtime) plus a single XML config/save file (`aoe_launcher_config.xml`) written
next to it. No installer, no registry entries, no other footprint.

**Honesty note:** written and reviewed carefully in an environment without
Windows, .NET, or internet access, so it has **not been compiled or run
yet** -- this includes the .NET Framework 4.8 retarget (from an original
.NET 8 version), which was done the same way: manually auditing every API
used against what .NET Framework 4.8 actually supports, and replacing
anything that wasn't (see "Notes on the .NET Framework 4.8 port" below).
Treat it as a solid draft that may need a short debugging pass on a real
machine. Send me any build error or odd behavior and I'll fix it directly
in the source.

## Features

- **Placement check, no registry/disk scanning**: the launcher ships inside
  the Ashes of Erebus folder itself, so its own location *is* the mod path.
  On startup it confirms: this folder is named exactly `Ashes of Erebus`,
  its parent is named `Mods`, and `Civ4BeyondSword.exe` exists two levels
  up. That last check catches the common Steam mistake of placing the mod
  at `...Beyond the Sword\Mods\Ashes of Erebus` instead of the correct
  `...Beyond the Sword\Beyond the Sword\Mods\Ashes of Erebus`. There's no
  manual override for any of this -- if placement is wrong, fix the
  placement (Re-check / Continue Anyway / Quit are the only options).
- **One-click launch**: runs `Civ4BeyondSword.exe` with the mod enabled via
  a direct process launch (`UseShellExecute = false`), not through
  `ShellExecuteEx`. An earlier version used `ShellExecuteEx` and produced a
  background process with no window that had to be killed from Task
  Manager, even though an identical manually-created shortcut launched
  fine; switching to a direct `CreateProcess`-style launch is a known fix
  for this class of symptom.
- **Launch button status**: the button shows the detected version from
  `version.txt` (e.g. `Launch Ashes of Erebus v380`), `v?` if that file is
  missing or malformed, or `Ashes of Erebus not found!` if
  `Civ4BeyondSword.exe` can't be located. Refresh re-evaluates it.
- **Close on launch?** checkbox (under Refresh): saved in the config file; when
  checked, the launcher exits right after successfully starting the game.
- **Drag and drop** between an Active list and an Inactive list to enable/
  disable modules. Drag a module folder in from Explorer to install it.
- **Per-module tooltip and details**: hovering a module shows its
  `shortdesc` from `info.txt`; clicking the **?** button on its row shows
  the full `desc`, version, author, RifE version, and compatibility list.
- **Update Schemas** (labeled "Dev: Update Schemas" in the UI, bottom-right):
  scans every module's `XML` folder (active and inactive) for files ending
  in `Schema.xml`, matches them against Ashes of Erebus's own base schema
  files (`Assets\XML`, *not* the base game's), and shows a preview of
  exactly what will change before touching anything -- Apply/Cancel, not
  the other way around. A module file like `Dao_CIV4TerrainSchema.xml` (or
  `D_CIV4TerrainSchema.xml`) maps to `CIV4TerrainSchema.xml` -- everything
  after the **last** underscore in the filename is treated as the base
  schema's name, since stock schema files never contain an underscore
  themselves but a module's prefix sometimes does. Folder structure mirrors
  exactly: `<module>\XML\<subpath>\<file>` maps to
  `Assets\XML\<subpath>\<parentFile>` (subpath may be empty, i.e. the file
  can sit directly under `XML\`). Both the preview and the final result
  report at the module level for modules with no problems, and at the
  individual-file level for modules that had one or more errors.
- **Presets**: save/load/delete named collections of the active module set.
- **Import/export via a compact share code**, formatted as
  `AoE<version>:<data>` where `<version>` comes from the mod's own
  `version.txt` (purely informational -- it doesn't block importing a
  preset made against a different version, just tells you). The payload
  itself is a small hand-rolled binary format, gzip-compressed
  and base64url-encoded, sized to comfortably fit inside Discord's
  2000-character message limit even with up to ~100 modules.
  - A **Futureproof** checkbox next to Export omits each module's version
    and change-fingerprint entirely. Importing a futureproof code just
    checks that each named module is present locally -- no "this looks
    different" warnings, since there's nothing to compare against.
- **Change detection tuned to how AoE modules are structured**: a
  lightweight fingerprint (see below) flags modules that have changed
  locally since a preset was saved, even if `info.txt`'s version number
  wasn't updated -- and specifically excludes `*Schema.xml` files, since
  those are expected to change independently via Update Schemas.
- **Dark theme**: dark grey background, white text, orange accents on
  buttons and highlights, matching the original launcher's look. Buttons
  use a custom `FlatButton` that suppresses the lingering keyboard-focus
  rectangle WinForms normally leaves after a click (it otherwise stays
  visible until some other control takes focus, reading as a stuck "bold"
  border). If you drop a `background.png` into `UI\Background\` inside the
  Ashes of Erebus folder, it's drawn pinned to the top-left corner of the
  window, unscaled -- revealed or clipped as you resize rather than
  stretched. The Active/Inactive module split is a fixed 50/50 with no
  draggable divider.

## `info.txt` format

Parsed as sectioned key/value blocks:

```
;comments start with a semicolon and are ignored
[version]
1.2
;
[shortdesc]
Cheaper earlier techs, MUCH more expensive late techs.
;
[desc]
Multi-line description text...
can span several lines, including blank ones for paragraph breaks.
```

`[shortdesc]` becomes the row's tooltip; `[desc]` (plus version/author/
rifeversion/compatible) shows up in the popup from that row's **?** button.

## Project layout

```
AoELauncher/
  AoELauncher.csproj
  Program.cs
  MainForm.cs              <- main window: module grids, drag/drop, presets, schemas
  Models/
    AppConfig.cs             <- the one config/save file's shape (Presets + close-on-launch flag)
    ModuleInfo.cs             <- live scan result, incl. parsed info.txt fields
    PlacementResult.cs        <- result of the startup placement check
  Core/
    ConfigManager.cs          <- load/save the XML config file (always next to the exe)
    CompatHelpers.cs          <- small .NET Framework 4.8 shims (hex encoding, relative paths)
    InstallLocator.cs         <- placement validation only, no registry/disk scanning
    ModuleScanner.cs          <- scans modules, parses info.txt, computes fingerprints
    SchemaUpdater.cs          <- the Update Schemas action
    PresetCodec.cs            <- compact binary encode/decode for the share string
    GameLauncher.cs           <- starts the game with the mod enabled
  UI/
    Theme.cs                  <- shared dark/orange color scheme
    PlacementIssuesForm.cs    <- shown when the startup placement check fails
    InputForm.cs              <- generic text-entry dialog (preset names, import)
```

## How to build it (Visual Studio)

1. Install **Visual Studio 2022** (the free Community edition works fine)
   with the ".NET desktop development" workload (this includes the .NET
   Framework 4.8 targeting pack).
2. Open `AoELauncher/AoELauncher.csproj`.
3. Right-click the project → **Publish** → Folder. There's no
   self-contained/single-file/runtime-identifier option to set here on
   purpose -- the project targets `net48` and is framework-dependent by
   default, so a normal publish (or even just a Release build) already
   produces a small `.exe` (well under 1MB) that relies on the target
   machine already having .NET Framework 4.8. That's effectively every
   Windows 10/11 machine, since 4.8 has shipped as a Windows Update
   component since 2019 -- there's deliberately no bundled runtime here,
   unlike an earlier version of this project that targeted .NET 8
   self-contained and produced a 60-150 MB exe.
4. Drop that one `.exe` into the `Ashes of Erebus` mod folder itself (next
   to its `Assets` folder) -- the launcher's own location is how it finds
   everything else. The first run creates `aoe_launcher_config.xml` right
   beside it.

## Notes on a few design decisions

- **Where the launcher must live**: directly inside the Ashes of Erebus mod
  folder (i.e. the folder that itself contains `Assets\Modules\...`). There
  is no way to point it elsewhere -- if you want the launcher accessible
  from somewhere else, make a shortcut to it.
- **No registry or disk scanning, no manual exe override**: the exe's own
  location tells us where the mod folder is; walking two levels up finds
  `Civ4BeyondSword.exe`. If that fails, the fix is to correct the folder
  placement, not to configure around it.
- **Fingerprint algorithm**: `*Schema.xml` files are excluded entirely
  (see Update Schemas above). Files under a module's top-level `Art` folder
  are checked by relative path + size only (large binary assets, too slow
  to hash by content on every export). Everything else -- the XML/txt
  gameplay data, where a single differing value can cause multiplayer
  desyncs -- gets a full SHA-256 content hash. Last-write timestamps are
  never used, since they don't reliably indicate an actual content change.
  The combined fingerprint is truncated to 8 hex characters (32 bits): a
  "did this change" signal, not a cryptographic guarantee, which is the
  right tradeoff here and also keeps preset codes compact.
- **Share code format**: single fixed payload format, no back-compat
  handling -- the `AoE<version>:` prefix is just the mod's version.txt
  contents for the user's information, not a wire-format version switch.
- **Module load order**: still not adjustable within the Active list. If
  AoE's module system is sensitive to load order, let me know and I'll add
  drag-to-reorder plus persist the order in the config/preset.
- **Permissions**: if AoE is installed under `Program Files`, moving module
  folders (or saving the config file) may require running the launcher as
  Administrator. Failures show a clear message suggesting this.
- **Dark theme limitation**: native WinForms `GroupBox` borders are
  OS-themed and don't fully recolor without owner-drawing the control --
  fills, text, buttons, and grids are fully themed, but the thin outline
  around "Active Modules"/"Inactive Modules" may not perfectly match.

## If something doesn't compile or behave right

Send me the build error or the behavior you're seeing and I'll fix it
directly in the source.
