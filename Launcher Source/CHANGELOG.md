# Changelog

## 1.1

- **Filters row placement**: the Filters row is now always shown directly
  beneath the module lists, never beneath the preset buttons. The filter row and
  the preset rows are one block with fixed positions, instead of two separate
  bottom-docked panels whose order depended on z-order.
- **Manage/Hide Modules button** shows the current preset: `Manage Modules
  (Core)` / `Hide Modules (Custom)`. A preset is current when the active modules
  are exactly its modules, in the Load #s it records, with the same content
  fingerprints (presets without fingerprints, i.e. futureproof, skip that
  check); otherwise it reads `Custom`. The button sizes itself to its text (up
  to a maximum width).
- **Column headers**: `Version` is now `M. Ver` and `AoE Rev` is now `AoE Ver`.
  All column headers have mouseover tooltips.
- **Info window** sizes itself to its text in both width and height (up to ~85%
  of the screen, then it scrolls) and is centered over the launcher window.
- **Module path scan**: modules hardcode paths into module folders
  (`Modules/<Load #>/<Module>/...`), including other modules'. When a Load #
  changes, those references are now corrected in all modules.
  - Only `.xml` files under each module's `XML` folder (never `*Schema.xml`) are
    scanned, and only elements whose whole content is a `Modules/...` path. A
    module's own paths are fixed when it is moved, using exactly the same rules
    and code as the full scan.
  - The full scan (active and inactive modules) always runs when a preset is
    saved, loaded, exported or imported, when the game is launched (after the
    module checks), and when Refresh is pressed. It does not run when modules
    are merely moved. There is no config flag.
  - The status bar shows the scan's progress, so a hang is easier to diagnose.
  - If an active module's files point into an inactive module, a notice names
    the pair (once per session; Refresh resets it): likely a missing dependency.
- **Presets**: a centered `Presets:` heading (styled like `Filters:`) sits below
  the separator line. Names are limited to 24 characters, and the dropdown is
  sized to match and centered in its row, with `Delete "<preset>"` on its left
  and `Load "<preset>"` on its right (both 125 wide, named after the selected
  preset, greyed out when there are none). Import Preset is centered under the
  dropdown, Export sits under Save at the same width, and the checkbox is now
  just `Futureproof`, with a tooltip. Saving with Futureproof checked saves a
  preset without versions or fingerprints (as if imported from a futureproof
  code), and then doesn't need the path scan.
- **Tooltips** on every button and checkbox. **Button sizes**: Instructions,
  Open Civ4 Config, Refresh, Update Schemas, Save and Export are sized to their
  text, and the window's minimum width is calculated from the actual widths.
- **Export Active Modules As Preset** (was Export Preset) exports the current
  active modules and their Load #s rather than a saved preset. If they match a
  saved preset (including fingerprints), its name is added to the code's id
  string, e.g. `AoE387[Core]:...`. 1.1 codes are not compatible with 1.0.
- **Import** offers `Don't save` (between OK and Cancel) to use a code without
  keeping it in your presets, then applies it: modules are moved, the path scan
  runs, and only then are fingerprints compared.
- **Right-click menu** acts on every selected module in that list for `Open
  containing folder(s)` and `Set Load #(s) to N`, and the text pluralizes.
  (Opening more than 5 folders at once asks for confirmation.)
- **Right-click menu separators** are now white.
- Launcher version is now 1.1.

## 1.0

- Initial release.
