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
- **Close on launch?** checkbox (centered under Open Civ4 Config): saved in the config file; when
  checked, the launcher exits right after successfully starting the game.
- **Status indicator** (centered under Instructions, mirroring the Close on launch
  checkbox): `Status: Ready` (green), `Status: Launched` (orange; replaces Ready while
  `Civ4BeyondSword.exe` is running -- only checked when you interact with the launcher:
  window activated, status hovered, modules refreshed or game launched, never on a timer),
  `Status: Install Error` (red; the game exe wasn't found or the launcher is in the wrong folder,
  as found by the startup check), `Status: Module Issue` (red; an active module is incompatible with
  another, or a hard dependency isn't active/installed) or `Status: Bad Order`
  (yellow; a hard or soft dependency is active but loads after the module that
  lists it). If several apply, the first in that order wins. Hovering it shows the
  same text as the matching popup. It is re-evaluated after every refresh, i.e. once
  after each batch of moves (drag/drop of several modules, loading a preset, autosort...),
  not once per module. The colors are `StatusGood` / `StatusError` / `StatusWarning` in
  `Theme.cs`.
- **Load #s**: modules live under `Assets\Modules` (active) or
  `Assets\Modules (Off)` (inactive), in a numbered folder `0` to `4`:
  `Assets\Modules\<#>\<module>`. The **Load #** column shows the number.
  The game loads `0` first, then `1`, `2`, `3`, `4`; within each folder modules
  load alphabetically by module *folder* name.
  Right-clicking a module offers `Set Load # to 0 / 1 / 2 / 3 / 4`
  (hiding the one it's already in) and moves it between those folders on
  its current side; with several rows selected the choice applies to all of
  them. Moving a module between Active and Inactive (drag, double-click, or
  presets) preserves its Load #. Modules dropped in from Explorer land in Load # `1`
  (`ModuleLayout.DefaultPass`). A module folder name must be unique across all
  Load #s on a side.
- **Load # path rewriting**: modules hardcode paths to their own files (e.g. a promotion's
  `<Button>Modules/1/MyModule/Art/...</Button>`), where the number is the Load #. When a module
  is moved to a different Load #, `Core/ModulePathRewriter.cs` silently rewrites every
  `Modules/<old>/<ModuleName>/` in the module's text files (`.xml .txt .py .ini .cfg .csv`) to the
  new number (either slash direction). Only a module's references to its *own* folder are changed;
  files are edited as raw bytes so encoding, BOM and line endings are preserved. A popup appears
  only if a file couldn't be updated. Module fingerprints blank out that number, so moving a module
  doesn't make it look changed to presets.
- **Game-running warning**: if `Civ4BeyondSword.exe` is running (checked fresh at that moment),
  pressing Launch or moving modules (drag/drop, Set Load #, presets, autosort) first shows a
  Continue / Abort popup (Abort is the default). Aborting a move changes nothing; aborting a preset
  apply leaves the modules as they were.
- **Autosort**: `Autosort active modules`, at the bottom of the right-click menu of
  either list, and offered as a button in the load order popup when launching or
  saving a preset with a bad order. Like Update Schemas, it first shows what it
  would change (which modules, from which Load # to which, and why) and only moves
  anything after Apply. It is a simple greedy method (`Core/AutosortPlanner.cs`),
  built for few, short dependency chains: only modules involved in a broken
  dependency are moved, and only to a different Load # on the active side. It
  builds two candidate fixes -- pushing dependents later, or pulling dependencies
  earlier -- and uses whichever moves fewer modules. If the dependencies form a
  loop, need more than Load # 0-4, or anything else goes wrong, it just reports that
  no solution was found and changes nothing. It never activates or deactivates
  anything, and doesn't try to fix incompatibilities or missing dependencies.
- **Module names**: the name shown in the lists is the `[name]` entry of the
  module's `info.txt` (the folder name is used if there is none). Presets and
  the file system still identify modules by folder name.
- **Dependency and incompatibility checks**: when you press Launch, Save
  Preset or Export Preset, the launcher first checks `[incompatible]` (no two
  modules in the set may list each other as incompatible), then `[dependency-hard]`
  (every dependency must be in the set -- one popup for missing ones -- and load
  before the module that needs it: lower Load #, or same Load # and earlier
  alphabetically by folder name), then load order, which covers hard dependencies
  that load too late together with `[dependency-soft]` ones (not required to be
  present, but any that are in the set must load before the module listing them).
  Each kind of problem is shown in a popup listing the modules involved, with
  Abort / Continue; the load order popup also offers Autosort (for Launch and Save,
  which check the active modules; after an applied autosort the order is re-checked).
  Export checks the preset's modules in the Load #s the preset records (modules not
  installed locally can't be checked), without Autosort, since that moves real folders.
- **Tag filters**: a **Filters** row under the module lists has a three-state box
  for each of `Civ (New)`, `Civ (Edit)`, `Art`, `Joke`, `Mechanics`, `Leader`, `Balance`
  and `Event`. These match the info.txt `[tags]` tokens `Civ(N)`, `Civ(E)`, `Art`, `Joke`,
  `Mech`, `Lead`, `Bal` and `Event` respectively (the list is `FilterTags` in `MainForm.cs`).
- **Columns**: the Version, AoE Rev, Load # and Info columns are sized from their
  header text in the current font and can't be resized. AoE Rev (numerically) and
  Load # (in load order) can be sorted by clicking the header; Version can't.
  The Module|Author divider can be dragged (updating live as you drag; it is the
  only adjustable divider): the Author width is kept identical in the
  active and inactive lists, saved in the config file (`AuthorColumnWidth`) and
  restored on startup; only the Module column grows/shrinks with the window.
  Click a box to cycle it: empty = no filter, white = whitelist
  (modules *without* the tag are filtered out), black = blacklist (modules *with*
  the tag are filtered out); right-click clears it. With several whitelisted tags a
  module must have all of them. Filtered-out modules are never removed: they are
  greyed out and sorted to the bottom of their list, and stay active/inactive as
  before, so a forgotten filter can't silently change what gets launched. Tags come
  from the `[tags]` section; the filters aren't saved between runs. The `AoE Rev`
  column shows the `[aoeversion]` line.
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
  including each module's Load #. Loading a preset puts modules in the
  recorded Load #s; a module with no recorded Load # stays in whichever one it's in.
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
[name]
Cheaper Techs
;
[author]
Blazenclaw
;
[version]
1.2
;
[aoeversion]
380
;
[tags]
Civ(N), Mech
;
[dependency-hard]
SomeOtherModuleFolder, AnotherModuleFolder
;
[dependency-soft]
OptionalModuleFolder
;
[incompatible]
ConflictingModuleFolder
;
[shortdesc]
Cheaper earlier techs, MUCH more expensive late techs.
;
[desc]
Multi-line description text...
can span several lines, including blank ones for paragraph breaks.
```

`[name]` is the module's display name. `[author]` fills the **Author** column.
`[dependency-hard]`, `[dependency-soft]` and `[incompatible]` are comma-separated lists of other modules'
exact *folder* names (not their `[name]`); either may be empty.
`[aoeversion]` fills the **AoE Rev** column. `[tags]` is a list separated by
commas, semicolons, pipes, spaces or line breaks; each entry is compared as a
whole word, case-insensitively, against the filter tags.

`[shortdesc]` becomes the row's tooltip; `[desc]` (plus version/author/
AoE version/compatible/dependencies/incompatible) shows up in the popup from that row's **?** button.

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
    ModuleLayout.cs           <- Load # (0-4) folder layout helpers
    ModulePathRewriter.cs     <- updates a module's own Modules/<Load #>/... paths when it changes Load #
    ModuleScanner.cs          <- scans modules, parses info.txt, computes fingerprints
    ModuleChecker.cs          <- [incompatible], [dependency-hard] and [dependency-soft] verification
    AutosortPlanner.cs        <- dry-run planner behind "Autosort active modules"
    SchemaUpdater.cs          <- the Update Schemas action
    PresetCodec.cs            <- compact binary encode/decode for the share string
    GameLauncher.cs           <- starts the game with the mod enabled
  UI/
    Theme.cs                  <- shared dark/orange color scheme (also styles tooltips and right-click menus)
    StatusIndicator.cs        <- the "Status: ..." readout with a separately colored value
    TagFilterBox.cs           <- three-state (neutral / whitelist / blacklist) tag filter box
    BufferedControls.cs       <- double-buffered Panel/GroupBox/SplitContainer
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
- **Module load order**: load order within a Load # isn't adjustable (it is
  alphabetical by folder name); the coarse ordering is the Load # (`0` to `4`),
  set via the right-click menu or Autosort and stored in presets.
- **Permissions**: if AoE is installed under `Program Files`, moving module
  folders (or saving the config file) may require running the launcher as
  Administrator. Failures show a clear message suggesting this.
- **Dark theme limitation**: native WinForms `GroupBox` borders are
  OS-themed and don't fully recolor without owner-drawing the control --
  fills, text, buttons, and grids are fully themed, but the thin outline
  around "Active Modules"/"Inactive Modules" may not perfectly match.