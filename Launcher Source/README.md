# Ashes of Erebus Launcher

A lightweight, standalone module manager and launcher for the Civilization IV mod
*Ashes of Erebus*. Ships as a single small `.exe` (targets .NET Framework 4.8,
framework-dependent -- not self-contained, so it stays well under 1MB and relies
on the .NET Framework already present on the machine rather than bundling a
runtime) plus a single XML config/save file (`aoe_launcher_config.xml`) written
next to it. No installer, no registry entries, no other footprint.

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
  a direct process launch (`UseShellExecute = false`)
- **Launch button status**: the button shows the detected version from
  `version.txt` (e.g. `Launch Ashes of Erebus v380`)
- **Manage Modules / Hide Modules** button (centered under Launch): shows or
  hides everything beneath it except the status bar -- the module lists and
  the preset/dev tools. Hidden, the window shrinks to just the top section
  (Instructions, Launch, Open Civ4 Config, Close on launch); shown, it grows
  back to its previous height. The state is saved in the config file
  (`ModulesVisible`) and applied on startup; it defaults to hidden.
- **Remembered window size**: the window's width, its height while the module
  section is shown, and whether it was maximized are saved in the config file
  (`WindowClientWidth`, `WindowClientHeight`, `WindowMaximized`) when the user
  finishes resizing, maximizes/restores, or closes the window, and are applied
  on the next startup (clamped to the screen). The hidden-modules height is
  fixed, so only the expanded height is stored.
- **Close on launch?** checkbox (under Open Civ4 Config): saved in the config file; when
  checked, the launcher exits right after successfully starting the game.
- **Load passes**: modules live under `Assets\Modules` (active) or
  `Assets\Modules (Off)` (inactive), in either `Def\<module>` (default) or
  `Seq\1..4\<module>` (sequenced). The **Loadpass** column shows `Default` or `1`-`4`.
  The game loads `Def` first, then `1`, `2`, `3`, `4`; within each folder modules
  load alphabetically by module *folder* name.
  Right-clicking a module offers `Load in pass: Default / 1 / 2 / 3 / 4`
  (hiding the pass it's already in) and moves it between those folders on
  its current side; with several rows selected the choice applies to all of
  them. Moving a module between Active and Inactive (drag, double-click, or
  presets) preserves its pass. Modules dropped in from Explorer land in `Def`.
  A module folder name must be unique across all passes on a side.
- **Module names**: the name shown in the lists is the `[name]` entry of the
  module's `info.txt` (the folder name is used if there is none). Presets and
  the file system still identify modules by folder name.
- **Dependency and incompatibility checks**: when you press Launch, Save
  Preset or Export Preset, the launcher first checks `[incompatible]` (no two
  modules in the set may list each other as incompatible), then `[dependency]`
  (every dependency must be in the set and load before the module that needs
  it: earlier pass, or same pass and earlier alphabetically by folder name).
  Each problem is shown in a popup listing the modules involved, with
  Abort / Continue. Launch and Save check the active modules; Export checks the
  preset's modules in the passes the preset records (modules not installed
  locally can't be checked).
- **Tag and revision columns**: `Civ`, `Mech`, `Art` and `Joke` show a
  checkmark when the module's `[tags]` section contains that tag; `AoE Rev`
  shows the `[aoeversion]` line.
- **Drag and drop** between an Active list and an Inactive list to enable/
  disable modules. Drag a module folder in from Explorer to install it.
- **Per-module tooltip and details**: hovering a module shows its
  `shortdesc` from `info.txt`; clicking the **?** button on its row shows
  the full `desc`, version, author, AoE version, and compatibility list.
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
- **Presets**: save/load/delete named collections of the active module set,
  including each module's load pass. Loading a preset puts modules in the
  recorded passes; a module with no recorded pass stays in whichever pass it's in.
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
[name]
Cheaper Techs
;
[shortdesc]
Cheaper earlier techs, MUCH more expensive late techs.
;
[aoeversion]
380
;
[tags]
Civ, Mech
;
[dependency]
Some Other Module, Another Module
;
[incompatible]
Conflicting Module
;
[desc]
Multi-line description text...
can span several lines, including blank ones for paragraph breaks.
```

`[name]` is the module's display name, and is also what other modules write in
their `[dependency]` and `[incompatible]` lists (comma-separated; both may be empty).
`[aoeversion]` fills the **AoE Rev** column. `[tags]` is a list separated by
commas, semicolons, pipes, spaces or line breaks; each entry is compared as a
whole word, case-insensitively, against `Civ`, `Mech`, `Art` and `Joke`.

`[shortdesc]` becomes the row's tooltip; `[desc]` (plus version/author/
AoE version/compatible/dependency/incompatible) shows up in the popup from that row's **?** button.

## Project layout

```
AoELauncher/
  AoELauncher.csproj
  Program.cs
  MainForm.cs              <- main window: module grids, drag/drop, presets, schemas
  Models/
    AppConfig.cs             <- the one config/save file's shape (Presets + close-on-launch + modules-visible + window size)
    ModuleInfo.cs             <- live scan result, incl. parsed info.txt fields
    PlacementResult.cs        <- result of the startup placement check
  Core/
    ConfigManager.cs          <- load/save the XML config file (always next to the exe)
    CompatHelpers.cs          <- small .NET Framework 4.8 shims (hex encoding, relative paths)
    InstallLocator.cs         <- placement validation only, no registry/disk scanning
    ModuleLayout.cs           <- Def\ / Seq\1..4 folder layout and load-pass helpers
    ModuleScanner.cs          <- scans modules, parses info.txt, computes fingerprints
    ModuleChecker.cs          <- [incompatible] and [dependency] verification
    SchemaUpdater.cs          <- the Update Schemas action
    PresetCodec.cs            <- compact binary encode/decode for the share string
    GameLauncher.cs           <- starts the game with the mod enabled
  UI/
    Theme.cs                  <- shared dark/orange color scheme
    PlacementIssuesForm.cs    <- shown when the startup placement check fails
    InputForm.cs              <- generic text-entry dialog (preset names, import)
```

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
- **Module load order**: load order within a pass isn't adjustable; the
  coarse ordering is the load pass (`Def`, then `Seq\1`-`4`), set via the
  right-click menu and stored in presets.
- **Permissions**: if AoE is installed under `Program Files`, moving module
  folders (or saving the config file) may require running the launcher as
  Administrator. Failures show a clear message suggesting this.
- **Dark theme limitation**: native WinForms `GroupBox` borders are
  OS-themed and don't fully recolor without owner-drawing the control --
  fills, text, buttons, and grids are fully themed, but the thin outline
  around "Active Modules"/"Inactive Modules" may not perfectly match.