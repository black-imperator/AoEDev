using System;
using System.Collections.Generic;
using System.Diagnostics;
using System.Drawing;
using System.IO;
using System.Linq;
using System.Reflection;
using System.Text;
using System.Text.RegularExpressions;
using System.Windows.Forms;
using AoELauncher.Core;
using AoELauncher.Models;
using AoELauncher.UI;

namespace AoELauncher;

public class MainForm : Form
{
    private readonly string _modPath =
        AppContext.BaseDirectory.TrimEnd(Path.DirectorySeparatorChar, Path.AltDirectorySeparatorChar);

    /// <summary>Resolved fresh from placement validation each run; never persisted or manually overridden.</summary>
    private string? _btsExePath;

    private const string LauncherVersion = "1.0";

    /// <summary>What a version.txt value must look like to be shown on the Launch button (a short single token such as "380").</summary>
    private static readonly Regex VersionPattern = new(@"^[0-9A-Za-z._-]{1,12}$");

    private AppConfig _config = new();
    private List<ModuleInfo> _activeModules = new();
    private List<ModuleInfo> _inactiveModules = new();

    private SplitContainer _splitContainer = null!;
    private ModuleGridView dgvActive = null!;
    private ModuleGridView dgvInactive = null!;
    private ComboBox cmbPresets = null!;
    private CheckBox chkFutureproof = null!;
    private Label lblStatus = null!;
    private Button btnLaunch = null!;
    private CheckBox chkCloseOnLaunch = null!;

    public MainForm()
    {
        Text = "Ashes of Erebus Launcher";
        Width = 980;
        Height = 700;
        StartPosition = FormStartPosition.CenterScreen;
        MinimumSize = new Size(880, 520);

        Theme.StyleForm(this);
        //LoadBackgroundImage(); // BLAZE disabled; seems winforms can't have alpha layers in foreground elements we need

        BuildUi();
        SetupDragDrop();

        Load += MainForm_Load;
    }

    /*
    private void LoadBackgroundImage()
    {
        try
        {
            var asm = Assembly.GetExecutingAssembly();
            using var stream = asm.GetManifestResourceStream("AoELauncher.UI.Background.background.png");
            if (stream == null) return;

            using var loaded = Image.FromStream(stream);
            BackgroundImage = new Bitmap(loaded); // detach from the stream so it's safe to dispose
            BackgroundImageLayout = ImageLayout.None; // pinned top-left, unscaled, clipped/revealed as the window resizes
        }
        catch
        {
            // Malformed or unreadable background image: just skip it, not worth failing startup over.
        }
    }
    */

    // ---------------------------------------------------------------- UI ---

    private void BuildUi()
    {
        var topPanel = new Panel { Dock = DockStyle.Top, Height = 100 };
        Theme.StyleContainer(topPanel);

        btnLaunch = new FlatButton
        {
            Text = "Launch Ashes of Erebus",
            Width = 480,
            Height = 72,
            Top = 14,
            Font = new Font(Font.FontFamily, Font.Size * 2f, FontStyle.Bold),
        };
        Theme.StyleButton(btnLaunch, primary: true);
        btnLaunch.Click += (s, e) => LaunchGame();

        var btnRefresh = new FlatButton { Text = "Refresh", Width = 90, Height = Theme.ButtonHeight, Top = 13 };
        Theme.StyleButton(btnRefresh);
        btnRefresh.Click += (s, e) => RefreshModules();

        // Sized from the measured text rather than AutoSize, so its width is already correct
        // when the Resize handler below right-aligns it (AutoSize only settles after layout).
        chkCloseOnLaunch = new CheckBox
        {
            Text = "Close on launch?",
            Top = 50,
            Height = 22,
        };
        chkCloseOnLaunch.Width = TextRenderer.MeasureText(chkCloseOnLaunch.Text, chkCloseOnLaunch.Font).Width + 24;
        Theme.StyleCheckBox(chkCloseOnLaunch);
        // The CheckedChanged handler (which saves the setting) is attached in MainForm_Load,
        // after the saved value has been applied, so loading the config doesn't trigger a save.

        var btnHelp = new FlatButton { Text = "Instructions", Left = 12, Top = 13, Width = 130, Height = Theme.ButtonHeight };
        Theme.StyleButton(btnHelp);
        btnHelp.Click += (s, e) => ShowHelp();

        topPanel.Controls.Add(btnHelp);
        topPanel.Controls.Add(btnLaunch);
        topPanel.Controls.Add(btnRefresh);
        topPanel.Controls.Add(chkCloseOnLaunch);
        topPanel.Resize += (s, e) =>
        {
            btnLaunch.Left = (topPanel.Width - btnLaunch.Width) / 2;
            btnRefresh.Left = topPanel.Width - btnRefresh.Width - 12;
            chkCloseOnLaunch.Left = topPanel.Width - chkCloseOnLaunch.Width - 12;
        };

        _splitContainer = new SplitContainer
        {
            Dock = DockStyle.Fill,
            Orientation = Orientation.Vertical,
            IsSplitterFixed = true, // panes are always an even 50/50 split -- no draggable divider
            SplitterWidth = 3,
        };
        Theme.StyleContainer(_splitContainer);
        _splitContainer.Resize += (s, e) => CenterSplitter();

        var activeGroup = new GroupBox { Text = "Active Modules (loaded in-game)", Dock = DockStyle.Fill };
        Theme.StyleContainer(activeGroup);
        dgvActive = CreateModuleGrid();
        activeGroup.Controls.Add(dgvActive);

        var inactiveGroup = new GroupBox { Text = "Inactive Modules (installed, not loaded)", Dock = DockStyle.Fill };
        Theme.StyleContainer(inactiveGroup);
        dgvInactive = CreateModuleGrid();
        inactiveGroup.Controls.Add(dgvInactive);

        _splitContainer.Panel1.Controls.Add(activeGroup);
        _splitContainer.Panel2.Controls.Add(inactiveGroup);

        var bottomPanel = new Panel { Dock = DockStyle.Bottom, Height = 88 };
        Theme.StyleContainer(bottomPanel);

        // Row 1: preset save/load/delete, with the dev action right-aligned on the same line
        var btnSave = new FlatButton { Text = "Save Active Modules As New Preset", Left = 12, Top = 8, Width = 250, Height = Theme.ButtonHeight };
        cmbPresets = new ComboBox { Left = 270, Top = 11, Width = 170, DropDownStyle = ComboBoxStyle.DropDownList };
        var btnLoad = new FlatButton { Text = "Load Preset", Left = 448, Top = 8, Width = 110, Height = Theme.ButtonHeight };
        var btnDelete = new FlatButton { Text = "Delete", Left = 566, Top = 8, Width = 80, Height = Theme.ButtonHeight };
        var btnCiv4Config = new FlatButton { Text = "Open Civ4 Config", Top = 8, Width = 150, Height = Theme.ButtonHeight };
        Theme.StyleButton(btnSave);
        Theme.StyleComboBox(cmbPresets);
        Theme.StyleButton(btnLoad);
        Theme.StyleButton(btnDelete);
        Theme.StyleButton(btnCiv4Config);
        btnCiv4Config.Click += (s, e) => OpenCiv4Config();

        // Row 2: import (left) / export (right)
        var btnImport = new FlatButton { Text = "Import Preset", Left = 12, Top = 44, Width = 135, Height = Theme.ButtonHeight };
        var btnExport = new FlatButton { Text = "Export Preset", Left = 155, Top = 44, Width = 135, Height = Theme.ButtonHeight };
        chkFutureproof = new CheckBox
        {
            Text = "Futureproof (omit version, skip change checks)",
            Left = 298, Top = 48, Width = 340,
        };
        var btnDevSchemas = new FlatButton { Text = "Dev: Update Schemas", Top = 44, Width = 170, Height = Theme.ButtonHeight };
        Theme.StyleButton(btnImport);
        Theme.StyleCheckBox(chkFutureproof);
        Theme.StyleButton(btnExport);
        Theme.StyleButton(btnDevSchemas);
        btnDevSchemas.Click += (s, e) => UpdateSchemas();

        btnSave.Click += (s, e) => SavePreset();
        btnLoad.Click += (s, e) => LoadPreset();
        btnDelete.Click += (s, e) => DeletePreset();
        btnExport.Click += (s, e) => ExportPreset();
        btnImport.Click += (s, e) => ImportPreset();

        bottomPanel.Controls.AddRange(new Control[]
        {
            btnSave, cmbPresets, btnLoad, btnDelete, btnCiv4Config, btnImport, btnExport, chkFutureproof, btnDevSchemas
        });
        bottomPanel.Resize += (s, e) => { btnCiv4Config.Left = bottomPanel.Width - btnCiv4Config.Width - 12; };
        bottomPanel.Resize += (s, e) => { btnDevSchemas.Left = bottomPanel.Width - btnDevSchemas.Width - 12; };

        // Status bar: status text fills the left, launcher version sits at the right.
        var statusPanel = new Panel { Dock = DockStyle.Bottom, Height = 26 };
        Theme.StyleContainer(statusPanel);

        lblStatus = new Label
        {
            Dock = DockStyle.Fill,
            TextAlign = ContentAlignment.MiddleLeft,
            Padding = new Padding(10, 0, 0, 0),
            Text = "",
        };
        Theme.StyleLabel(lblStatus, muted: true);
        lblStatus.BackColor = Theme.Panel;

        var lblLauncherVersion = new Label
        {
            Dock = DockStyle.Right,
            AutoSize = true,
            TextAlign = ContentAlignment.MiddleRight,
            Padding = new Padding(0, 0, 10, 0),
            Text = $"Launcher v{LauncherVersion}",
        };
        Theme.StyleLabel(lblLauncherVersion, muted: true);
        lblLauncherVersion.BackColor = Theme.Panel;

        // Fill control goes in first so the Right-docked label claims its space before it.
        statusPanel.Controls.Add(lblStatus);
        statusPanel.Controls.Add(lblLauncherVersion);

        Controls.Add(_splitContainer);
        Controls.Add(bottomPanel);
        Controls.Add(statusPanel);
        Controls.Add(topPanel);
    }

    /// <summary>
    /// Keeps the two panes an even 50/50 split. When the window is minimized (or otherwise
    /// squeezed very small) the container's width can drop below Panel1MinSize + Panel2MinSize +
    /// SplitterWidth, at which point NO SplitterDistance is valid and assigning one throws. In
    /// that case there's nothing sensible to do, so leave it alone; the container fires Resize
    /// again on restore and the split is re-centered then.
    /// </summary>
    private void CenterSplitter()
    {
        var min = _splitContainer.Panel1MinSize;
        var max = _splitContainer.Width - _splitContainer.Panel2MinSize - _splitContainer.SplitterWidth;
        if (max < min) return;

        var target = Math.Max(min, Math.Min(_splitContainer.Width / 2, max));
        if (_splitContainer.SplitterDistance != target)
            _splitContainer.SplitterDistance = target;
    }

    private static ModuleGridView CreateModuleGrid()
    {
        var grid = new ModuleGridView
        {
            Dock = DockStyle.Fill,
            AllowDrop = true,
            AllowUserToAddRows = false,
            AllowUserToDeleteRows = false,
            AllowUserToResizeRows = false,
            ColumnHeadersHeightSizeMode = DataGridViewColumnHeadersHeightSizeMode.DisableResizing,
            SelectionMode = DataGridViewSelectionMode.FullRowSelect,
            MultiSelect = true,
            ReadOnly = true,
            RowHeadersVisible = false,
            AutoSizeColumnsMode = DataGridViewAutoSizeColumnsMode.None,
            BorderStyle = BorderStyle.None,
            CellBorderStyle = DataGridViewCellBorderStyle.SingleHorizontal,
            ShowCellToolTips = true,
        };
        Theme.StyleGrid(grid);

        var nameCol = new DataGridViewTextBoxColumn
        {
            Name = "Name", HeaderText = "Module",
            AutoSizeMode = DataGridViewAutoSizeColumnMode.Fill,
            Resizable = DataGridViewTriState.False,
        };
        var versionCol = new DataGridViewTextBoxColumn
        {
            Name = "Version", HeaderText = "Version",
            AutoSizeMode = DataGridViewAutoSizeColumnMode.None,
            Width = 72,
            Resizable = DataGridViewTriState.False,
        };
        var infoCol = new DataGridViewButtonColumn
        {
            Name = "Info",
            HeaderText = "Info",
            AutoSizeMode = DataGridViewAutoSizeColumnMode.None,
            Width = 32,
            Resizable = DataGridViewTriState.False,
            FlatStyle = FlatStyle.Flat,
        };

        grid.Columns.AddRange(nameCol, versionCol, infoCol);
        return grid;
    }

    // ---------------------------------------------------------- Lifecycle ---

    private void MainForm_Load(object? sender, EventArgs e)
    {
        _config = ConfigManager.Load();

        chkCloseOnLaunch.Checked = _config.CloseOnLaunch;
        chkCloseOnLaunch.CheckedChanged += (s, args) =>
        {
            _config.CloseOnLaunch = chkCloseOnLaunch.Checked;
            SaveConfig();
        };

        var placement = InstallLocator.ValidatePlacement(_modPath);
        if (!placement.IsValid)
        {
            if (!ResolvePlacementIssues(placement))
            {
                Close();
                return;
            }
        }
        else
        {
            _btsExePath = placement.BtsExePath;
        }

        RefreshModules(true);
        RefreshPresetCombo();
    }

    /// <summary>Returns true if the app should proceed, false if the user chose to quit.</summary>
    private bool ResolvePlacementIssues(PlacementResult initial)
    {
        var placement = initial;
        while (true)
        {
            var msg = new StringBuilder();
            msg.AppendLine("The launcher found some problems with where this folder is placed:");
            msg.AppendLine();
            foreach (var err in placement.Errors)
            {
                msg.AppendLine(err);
                msg.AppendLine();
            }
            msg.AppendLine("Move or rename the folder as needed, then choose Re-check, or continue anyway if you " +
                            "know what you're doing (launching the game won't work until this is fixed).");

            using var dlg = new PlacementIssuesForm(msg.ToString());
            dlg.ShowDialog(this);

            switch (dlg.Choice)
            {
                case PlacementChoice.Recheck:
                    placement = InstallLocator.ValidatePlacement(_modPath);
                    if (placement.IsValid)
                    {
                        _btsExePath = placement.BtsExePath;
                        return true;
                    }
                    continue;

                case PlacementChoice.ContinueAnyway:
                    _btsExePath = placement.BtsExePath; // may still be null, that's fine -- Launch will just report it clearly
                    return true;

                case PlacementChoice.Quit:
                default:
                    return false;
            }
        }
    }

    private void SaveConfig()
    {
        try
        {
            ConfigManager.Save(_config);
        }
        catch (Exception ex)
        {
            MessageBox.Show(this,
                $"Couldn't save the launcher's settings file:\n{ex.Message}\n\n" +
                "Make sure this folder isn't read-only (running as Administrator can help if it's under Program Files).",
                "Save Failed", MessageBoxButtons.OK, MessageBoxIcon.Warning);
        }
    }

    private string ReadModVersion()
    {
        try
        {
            var path = Path.Combine(_modPath, "version.txt");
            if (File.Exists(path))
                return File.ReadAllText(path).Trim();
        }
        catch
        {
            // fall through
        }
        return "unknown";
    }

    /// <summary>
    /// Sets the Launch button text: "not found" when the game executable can't be located,
    /// otherwise the version from version.txt, or "v?" if that file is missing or malformed.
    /// </summary>
    private void UpdateLaunchButtonText()
    {
        if (_btsExePath == null || !File.Exists(_btsExePath))
        {
            btnLaunch.Text = "Ashes of Erebus not found!";
            return;
        }

        var version = ReadModVersion();
        var valid = version != "unknown" && VersionPattern.IsMatch(version);
        btnLaunch.Text = $"Launch Ashes of Erebus v{(valid ? version : "?")}";
    }

    // ------------------------------------------------------------- Launch ---

    private void LaunchGame()
    {
        if (_btsExePath == null || !File.Exists(_btsExePath))
        {
            MessageBox.Show(this,
                "The game location couldn't be found. This usually means the mod folder isn't placed correctly " +
                "-- restart the launcher to re-run the setup check.",
                "Cannot Launch", MessageBoxButtons.OK, MessageBoxIcon.Error);
            return;
        }

        try
        {
            var modFolderName = Path.GetFileName(_modPath);
            GameLauncher.Launch(_btsExePath, modFolderName);
            lblStatus.Text = "Launching Civilization IV...";

            if (_config.CloseOnLaunch)
                Close();
        }
        catch (Exception ex)
        {
            MessageBox.Show(this, $"Failed to launch the game:\n{ex.Message}", "Launch Error",
                MessageBoxButtons.OK, MessageBoxIcon.Error);
        }
    }

    // ------------------------------------------------------------ Modules ---

    private void RefreshModules(bool firstLaunch = false)
    {
        Cursor = Cursors.WaitCursor;
        lblStatus.Text = "Scanning modules...";
        UpdateLaunchButtonText();

        var activeScroll = SafeScrollIndex(dgvActive);
        var inactiveScroll = SafeScrollIndex(dgvInactive);
        var activeSelected = SelectedNames(dgvActive);
        var inactiveSelected = SelectedNames(dgvInactive);

        var all = ModuleScanner.ScanAll(_modPath);
        _activeModules = all.Where(m => m.IsActive).OrderBy(m => m.Name, StringComparer.OrdinalIgnoreCase).ToList();
        _inactiveModules = all.Where(m => !m.IsActive).OrderBy(m => m.Name, StringComparer.OrdinalIgnoreCase).ToList();

        PopulateGrid(dgvActive, _activeModules, activeSelected, activeScroll);
        PopulateGrid(dgvInactive, _inactiveModules, inactiveSelected, inactiveScroll);

        if (firstLaunch)
            lblStatus.Text = $"Drag modules between the two lists, or drag a module folder in from Explorer to install it.";
        else
            lblStatus.Text = $"{_activeModules.Count} active, {_inactiveModules.Count} inactive modules.";

        Cursor = Cursors.Default;
    }

    private static int SafeScrollIndex(DataGridView grid) =>
        grid.Rows.Count > 0 ? grid.FirstDisplayedScrollingRowIndex : 0;

    private static HashSet<string> SelectedNames(DataGridView grid) =>
        new(grid.SelectedRows.Cast<DataGridViewRow>().Select(r => ((ModuleInfo)r.Tag!).Name), StringComparer.OrdinalIgnoreCase);

    /// <summary>Repopulates a grid while preserving scroll position and selection where possible (both otherwise reset on Rows.Clear()).</summary>
    private static void PopulateGrid(DataGridView grid, List<ModuleInfo> modules, HashSet<string> selectedNames, int scrollIndex)
    {
        grid.Rows.Clear();
        foreach (var m in modules)
        {
            var infoText = !string.IsNullOrWhiteSpace(m.Desc) ? "i" : "";
            var idx = grid.Rows.Add(m.Name, m.Version, infoText);
            var row = grid.Rows[idx];
            row.Tag = m;
            if (!string.IsNullOrWhiteSpace(m.ShortDesc))
            {
                row.Cells["Name"].ToolTipText = m.ShortDesc;
                row.Cells["Version"].ToolTipText = m.ShortDesc;
            }
            // Explicitly set true/false (not just conditionally true): DataGridView can
            // auto-select the first row as a side effect of adding rows/assigning the
            // current cell, and leaving that implicit rather than overriding it here caused
            // the top row to end up selected after every refresh even when nothing should be.
            row.Selected = selectedNames.Contains(m.Name);
        }

        if (grid.Rows.Count > 0)
        {
            var clamped = Math.Max(0, Math.Min(scrollIndex, grid.Rows.Count - 1));
            try { grid.FirstDisplayedScrollingRowIndex = clamped; }
            catch { /* can throw if the grid isn't visible/sized yet, e.g. during startup */ }
        }
    }

    private void ShowModuleDetails(ModuleInfo m)
    {
        var text = new StringBuilder();
        text.AppendLine($"Version: {m.Version}");
        if (!string.IsNullOrWhiteSpace(m.Author)) text.AppendLine($"Author: {m.Author}");
        if (!string.IsNullOrWhiteSpace(m.RifeVersion)) text.AppendLine($"RifE version: {m.RifeVersion}");
        if (m.Compatible.Count > 0) text.AppendLine($"Compatible with: {string.Join(", ", m.Compatible)}");
        text.AppendLine();
        text.AppendLine(!string.IsNullOrWhiteSpace(m.Desc)
            ? m.Desc
            : (!string.IsNullOrWhiteSpace(m.ShortDesc) ? m.ShortDesc : "(no description provided)"));

        ShowScrollableMessage(m.Name, text.ToString());
    }

    // NOTE: this is a verbatim string literal (@"..."), so every character between the quotes
    // -- including line breaks and leading whitespace -- is taken literally as part of the
    // text. That's why the lines below sit flush against the left margin rather than indented
    // to match the surrounding code: any indentation here would show up as indentation in the
    // dialog itself.
    private void ShowHelp()
    {
        var msg = @"    GENERAL
- You can launch the game by the top center button; be aware it may take some time to activate
- Active modules are shown on the left panel, and inactive modules on the right panel
- The Open Civ4 Config button opens your Civ4 config .ini file in your default text editor

    USING MODULES
- Changing the status of a module simply makes this launcher move the game files for you; it can be done manually
- You can either doubleclick a module to move which side it is on, or click and drag it across
- Shift clicking a module with one already selected will select it and all modules between the two
- Control-clicking a module will toggle the selection of that specific module
- The Refresh button will update the shown module list if you manually move files with the launcher open

    PRESETS
- Pressing the ""Save..."" button will give you the option to save the current selection as a preset
- Pressing the Load Preset button will cause the currently selected preset in the dropdown box to be loaded
- Delete will prompt you whether to delete the currently selected preset

    EXPORTING AND IMPORTING
- Presets can be exported or imported, which is VERY USEFUL when you are reporting bugs on discord
- The Import Preset button will prompt you to paste a preset code, and then save and load it
- Export Preset will copy a code to your clipboard that you can use to send to others
- If the Futureproof box is checked, the copied code will not be checked upon import for matching module versions

    UPDATING SCHEMAS (For module makers)
- This button will attempt to *update*, not add, schema files for all modules. Please format your module correctly!";

        ShowScrollableMessage("Usage Guide", msg);
    }

    /// <summary>
    /// Normalizes any mix of bare \n, bare \r, or \r\n line endings to Environment.NewLine.
    /// ReadOnlySelectableTextBox wraps a RichTextBox (the usual way to get read-only,
    /// *selectable* text, since a plain Label can't be selected) -- and RichTextBox silently
    /// drops line breaks that are a bare \n with no \r. That's exactly what text coming from a
    /// module's Desc field tends to be, since it's often authored/edited on a non-Windows
    /// machine. Routing every string through here before it reaches the box, rather than
    /// patching individual call sites, is what actually fixes that for good.
    /// </summary>
    private static string NormalizeNewlines(string text) =>
        text.Replace("\r\n", "\n").Replace("\r", "\n").Replace("\n", Environment.NewLine);

    /// <summary>Generic scrollable read-only message dialog, styled to match the app, with a single OK button.</summary>
    private void ShowScrollableMessage(string title, string text)
    {
        using var form = new Form
        {
            Text = title,
            Width = 600,
            Height = 480,
            StartPosition = FormStartPosition.CenterParent,
        };
        Theme.StyleForm(form);

        var box = new ReadOnlySelectableTextBox
        {
            Dock = DockStyle.Fill,
            ScrollBars = ScrollBars.Vertical,
            Text = NormalizeNewlines(text),
            BorderStyle = BorderStyle.None,
        };
        box.BackColor = Theme.Panel;
        box.ForeColor = Theme.Text;

        var okBtn = new FlatButton { Text = "OK", Dock = DockStyle.Bottom, Height = 34, DialogResult = DialogResult.OK };
        Theme.StyleButton(okBtn, primary: true);

        form.Controls.Add(box);
        form.Controls.Add(okBtn);
        form.AcceptButton = okBtn;
        form.ShowDialog(this);
    }

    /// <summary>Same as ShowScrollableMessage but with Apply/Cancel, returning true if the user confirmed.</summary>
    private bool ShowConfirmMessage(string title, string text, string confirmText = "Apply", string cancelText = "Cancel")
    {
        using var form = new Form
        {
            Text = title,
            Width = 620,
            Height = 500,
            StartPosition = FormStartPosition.CenterParent,
        };
        Theme.StyleForm(form);

        var box = new ReadOnlySelectableTextBox
        {
            Dock = DockStyle.Fill,
            ScrollBars = ScrollBars.Vertical,
            Text = NormalizeNewlines(text),
            BorderStyle = BorderStyle.None,
        };
        box.BackColor = Theme.Panel;
        box.ForeColor = Theme.Text;

        var buttonPanel = new Panel { Dock = DockStyle.Bottom, Height = 44 };
        Theme.StyleContainer(buttonPanel);

        var confirmBtn = new FlatButton { Text = confirmText, DialogResult = DialogResult.OK, Width = 110, Height = Theme.ButtonHeight, Top = 7 };
        var cancelBtn = new FlatButton { Text = cancelText, DialogResult = DialogResult.Cancel, Width = 110, Height = Theme.ButtonHeight, Top = 7 };
        Theme.StyleButton(confirmBtn, primary: true);
        Theme.StyleButton(cancelBtn);
        buttonPanel.Resize += (s, e) =>
        {
            cancelBtn.Left = buttonPanel.Width - cancelBtn.Width - 12;
            confirmBtn.Left = cancelBtn.Left - confirmBtn.Width - 8;
        };
        buttonPanel.Controls.Add(confirmBtn);
        buttonPanel.Controls.Add(cancelBtn);

        form.Controls.Add(box);
        form.Controls.Add(buttonPanel);
        form.AcceptButton = confirmBtn;
        form.CancelButton = cancelBtn;

        return form.ShowDialog(this) == DialogResult.OK;
    }

    // ------------------------------------------------------------- Schemas ---

    private void UpdateSchemas()
    {
        var allModules = _activeModules.Concat(_inactiveModules).ToList();

        Cursor = Cursors.WaitCursor;
        var plan = SchemaUpdater.Plan(_modPath, allModules);
        Cursor = Cursors.Default;

        if (plan.ModuleReports.Count == 0)
        {
            ShowScrollableMessage("Update Schemas", "Every schema file already matches the base mod -- nothing to update.");
            return;
        }

        var preview = new StringBuilder();
        var modulesWithUpdates = plan.ModuleReports.Count(r => r.UpdatedCount > 0);
        preview.AppendLine($"This will update {plan.TotalPlannedUpdates} schema file(s) across {modulesWithUpdates} module(s).");
        if (plan.TotalErrors > 0)
            preview.AppendLine($"{plan.TotalErrors} file(s) have no matching base schema and will be skipped -- see below.");
        preview.AppendLine();

        foreach (var m in plan.ModuleReports.OrderBy(m => m.ModuleName, StringComparer.OrdinalIgnoreCase))
        {
            if (m.Errors.Count == 0)
            {
                preview.AppendLine($"{m.ModuleName}: {m.UpdatedCount} schema file(s) will be updated.");
            }
            else
            {
                preview.AppendLine($"{m.ModuleName}: {m.UpdatedCount} will be updated, {m.Errors.Count} skipped:");
                foreach (var err in m.Errors)
                    preview.AppendLine($"   - {err}");
            }
        }

        if (!ShowConfirmMessage("Update Schemas - Confirm", preview.ToString(), "Apply", "Cancel"))
            return;

        Cursor = Cursors.WaitCursor;
        var result = SchemaUpdater.Apply(plan);
        Cursor = Cursors.Default;

        lblStatus.Text = $"Schemas updated: {result.TotalUpdated} file(s)" +
            (result.TotalErrors > 0 ? $", {result.TotalErrors} error(s)." : ".");

        if (result.TotalErrors > 0)
        {
            var errText = new StringBuilder();
            errText.AppendLine("Some files couldn't be copied:");
            foreach (var m in result.ErrorReports)
            {
                errText.AppendLine($"{m.ModuleName}:");
                foreach (var err in m.Errors) errText.AppendLine($"   - {err}");
            }
            ShowScrollableMessage("Update Schemas - Errors", errText.ToString());
        }
    }

    // --------------------------------------------------------- Drag/drop ---
    // Selection logic (Ctrl-click toggle, Shift-click range, plain-click collapse, and
    // deferring that collapse when a drag might follow) lives in ModuleGridView itself --
    // see the comment on that class for why it has to be done there rather than here.

    private void SetupDragDrop()
    {
        ConfigureModuleGrid(dgvActive, isActiveList: true);
        ConfigureModuleGrid(dgvInactive, isActiveList: false);
    }

    private void ConfigureModuleGrid(ModuleGridView grid, bool isActiveList)
    {
        grid.DragThresholdReached += (s, e) =>
        {
            var paths = grid.SelectedRows.Cast<DataGridViewRow>()
                .Select(r => ((ModuleInfo)r.Tag!).FullPath)
                .ToList();
            if (paths.Count == 0) return;
            grid.DoDragDrop(new DataObject("AoEModulePaths", paths), DragDropEffects.Move);
        };

        grid.DragEnter += (s, e) =>
        {
            e.Effect = (e.Data!.GetDataPresent("AoEModulePaths") || e.Data.GetDataPresent(DataFormats.FileDrop))
                ? DragDropEffects.Move
                : DragDropEffects.None;
        };

        grid.DragDrop += (s, e) =>
        {
            if (e.Data!.GetDataPresent("AoEModulePaths"))
            {
                var paths = (List<string>)e.Data.GetData("AoEModulePaths")!;
                MoveModules(paths, toActive: isActiveList);
            }
            else if (e.Data.GetDataPresent(DataFormats.FileDrop))
            {
                var dropped = (string[])e.Data.GetData(DataFormats.FileDrop)!;
                InstallDroppedModules(dropped, toActive: isActiveList);
            }
        };

        grid.CellContentClick += (s, e) =>
        {
            if (e.RowIndex < 0) return;
            if (grid.Columns[e.ColumnIndex].Name != "Info") return;
            if (grid.Rows[e.RowIndex].Tag is ModuleInfo m && !string.IsNullOrWhiteSpace(m.Desc))
                ShowModuleDetails(m);
        };

        var contextMenu = new ContextMenuStrip();
        var openFolderItem = new ToolStripMenuItem("Open containing folder");
        contextMenu.Items.Add(openFolderItem);

        // Row index captured by the most recent right-click, so the click handler below
        // knows which row's folder to open regardless of the current selection.
        var contextRowIndex = -1;

        grid.MouseDown += (s, e) =>
        {
            // HitTest (rather than CellMouseDown) so this also correctly resets to -1 on a
            // right-click below the last row, where CellMouseDown never fires at all.
            contextRowIndex = e.Button == MouseButtons.Right ? grid.HitTest(e.X, e.Y).RowIndex : -1;
        };

        contextMenu.Opening += (s, e) =>
        {
            // Right-clicked empty space below the rows, or a header -- nothing to open.
            if (contextRowIndex < 0 || contextRowIndex >= grid.Rows.Count)
                e.Cancel = true;
        };

        openFolderItem.Click += (s, e) =>
        {
            if (contextRowIndex >= 0 && contextRowIndex < grid.Rows.Count &&
                grid.Rows[contextRowIndex].Tag is ModuleInfo m)
            {
                OpenModuleFolder(m.FullPath);
            }
        };

        grid.ContextMenuStrip = contextMenu;

        grid.CellDoubleClick += (s, e) =>
        {
            if (e.RowIndex < 0 || grid.Columns[e.ColumnIndex].Name == "Info") return;
            if (grid.Rows[e.RowIndex].Tag is ModuleInfo m)
                MoveModules(new List<string> { m.FullPath }, toActive: !isActiveList);
        };
    }

    /// <summary>
    /// Opens the Civ4 config .ini via the shortcut two levels above the mod folder
    /// (..\..\_Civ4Config, i.e. next to Civ4BeyondSword.exe). The shell follows the shortcut and
    /// opens its target with the user's default program for .ini files, so there's no need to
    /// resolve the .lnk ourselves. Tries "_Civ4Config.lnk" first, then a bare "_Civ4Config" in case
    /// it's a differently-made link or the file itself.
    /// </summary>
    private void OpenCiv4Config()
    {
        var basePath = Path.GetFullPath(Path.Combine(_modPath, "..", "..", "_Civ4Config"));
        var path = new[] { basePath + ".lnk", basePath }.FirstOrDefault(File.Exists);

        if (path == null)
        {
            MessageBox.Show(this,
                $"Couldn't find the Civ4 config shortcut. Expected it at:\n{basePath}.lnk",
                "Config Not Found", MessageBoxButtons.OK, MessageBoxIcon.Warning);
            return;
        }

        try
        {
            Process.Start(new ProcessStartInfo(path) { UseShellExecute = true });
        }
        catch (Exception ex)
        {
            MessageBox.Show(this, $"Couldn't open the Civ4 config:\n{ex.Message}", "Error",
                MessageBoxButtons.OK, MessageBoxIcon.Error);
        }
    }

    private void OpenModuleFolder(string path)
    {
        try
        {
            if (!Directory.Exists(path))
            {
                MessageBox.Show(this,
                    "This module's folder couldn't be found. It may have been moved, renamed, or deleted.",
                    "Folder Not Found", MessageBoxButtons.OK, MessageBoxIcon.Warning);
                return;
            }

            Process.Start(new ProcessStartInfo("explorer.exe", $"\"{path}\"") { UseShellExecute = true });
        }
        catch (Exception ex)
        {
            MessageBox.Show(this, $"Couldn't open that folder:\n{ex.Message}", "Error",
                MessageBoxButtons.OK, MessageBoxIcon.Error);
        }
    }

    private void MoveModules(List<string> sourcePaths, bool toActive)
    {
        var targetDir = toActive
            ? Path.Combine(_modPath, "Assets", "Modules", "NormalModules")
            : Path.Combine(_modPath, "Assets", "Inactive Modules", "NormalModules");
        Directory.CreateDirectory(targetDir);

        var errors = new List<string>();
        foreach (var src in sourcePaths)
        {
            try
            {
                var name = Path.GetFileName(src.TrimEnd(Path.DirectorySeparatorChar, Path.AltDirectorySeparatorChar));
                var dest = Path.Combine(targetDir, name);

                if (string.Equals(
                        Path.GetFullPath(src).TrimEnd('\\'),
                        Path.GetFullPath(dest).TrimEnd('\\'),
                        StringComparison.OrdinalIgnoreCase))
                {
                    continue; // already there
                }

                if (Directory.Exists(dest))
                {
                    errors.Add($"{name}: a module with this name already exists at the destination.");
                    continue;
                }

                Directory.Move(src, dest);
            }
            catch (Exception ex)
            {
                errors.Add($"{Path.GetFileName(src)}: {ex.Message}");
            }
        }

        if (errors.Count > 0)
        {
            MessageBox.Show(this, "Some modules couldn't be moved:\n\n" + string.Join("\n", errors) +
                "\n\nIf this keeps happening, try running the launcher as Administrator " +
                "(this can happen when the game is installed under Program Files).",
                "Move Modules", MessageBoxButtons.OK, MessageBoxIcon.Warning);
        }

        RefreshModules();
    }

    private void InstallDroppedModules(string[] droppedPaths, bool toActive)
    {
        var targetDir = toActive
            ? Path.Combine(_modPath, "Assets", "Modules", "NormalModules")
            : Path.Combine(_modPath, "Assets", "Inactive Modules", "NormalModules");
        Directory.CreateDirectory(targetDir);

        var errors = new List<string>();
        foreach (var path in droppedPaths)
        {
            try
            {
                if (!Directory.Exists(path))
                {
                    errors.Add($"{Path.GetFileName(path)}: only module folders can be dropped, not individual files.");
                    continue;
                }

                var name = Path.GetFileName(path.TrimEnd(Path.DirectorySeparatorChar, Path.AltDirectorySeparatorChar));
                var dest = Path.Combine(targetDir, name);

                if (Directory.Exists(dest))
                {
                    errors.Add($"{name}: a module with this name already exists.");
                    continue;
                }

                CopyDirectory(path, dest);
            }
            catch (Exception ex)
            {
                errors.Add($"{Path.GetFileName(path)}: {ex.Message}");
            }
        }

        if (errors.Count > 0)
        {
            MessageBox.Show(this, "Some items couldn't be installed:\n\n" + string.Join("\n", errors),
                "Install Modules", MessageBoxButtons.OK, MessageBoxIcon.Warning);
        }

        RefreshModules();
    }

    private static void CopyDirectory(string sourceDir, string destDir)
    {
        Directory.CreateDirectory(destDir);
        foreach (var file in Directory.GetFiles(sourceDir))
            File.Copy(file, Path.Combine(destDir, Path.GetFileName(file)), overwrite: false);
        foreach (var dir in Directory.GetDirectories(sourceDir))
            CopyDirectory(dir, Path.Combine(destDir, Path.GetFileName(dir)));
    }

    // ------------------------------------------------------------ Presets ---

    private void RefreshPresetCombo()
    {
        cmbPresets.Items.Clear();
        foreach (var p in _config.Presets.OrderBy(p => p.Name, StringComparer.OrdinalIgnoreCase))
            cmbPresets.Items.Add(p.Name);
        if (cmbPresets.Items.Count > 0) cmbPresets.SelectedIndex = 0;
    }

    private Preset? GetSelectedPreset()
    {
        if (cmbPresets.SelectedItem is not string name)
        {
            MessageBox.Show(this, "Select a preset first.", "No Preset Selected",
                MessageBoxButtons.OK, MessageBoxIcon.Information);
            return null;
        }
        return _config.Presets.FirstOrDefault(p => p.Name == name);
    }

    private void SavePreset()
    {
        var name = InputForm.Prompt(this, "Save Preset", "Preset name:", "");
        if (string.IsNullOrWhiteSpace(name)) return;
        name = name!.Trim();

        var existing = _config.Presets.FirstOrDefault(p => p.Name.Equals(name, StringComparison.OrdinalIgnoreCase));
        if (existing != null)
        {
            var confirm = MessageBox.Show(this, $"A preset named '{name}' already exists. Overwrite it?",
                "Overwrite Preset", MessageBoxButtons.YesNo, MessageBoxIcon.Question);
            if (confirm != DialogResult.Yes) return;
            _config.Presets.Remove(existing);
        }

        Cursor = Cursors.WaitCursor;
        var preset = new Preset { Name = name, SourceVersion = ReadModVersion() };
        foreach (var m in _activeModules)
        {
            preset.Modules.Add(new ModuleRef
            {
                Name = m.Name,
                Version = m.Version,
                Fingerprint = ModuleScanner.ComputeFingerprint(m.FullPath),
            });
        }
        Cursor = Cursors.Default;

        _config.Presets.Add(preset);
        SaveConfig();
        RefreshPresetCombo();
        cmbPresets.SelectedItem = preset.Name;
        lblStatus.Text = $"Saved preset '{preset.Name}' with {preset.Modules.Count} modules.";
    }

    private void LoadPreset()
    {
        var preset = GetSelectedPreset();
        if (preset == null) return;
        ApplyPreset(preset);
    }

    private void ApplyPreset(Preset preset)
    {
        var wanted = new HashSet<string>(preset.Modules.Select(m => m.Name), StringComparer.OrdinalIgnoreCase);

        var beforeCurrent = _activeModules.Concat(_inactiveModules)
            .GroupBy(m => m.Name, StringComparer.OrdinalIgnoreCase)
            .ToDictionary(g => g.Key, g => g.First(), StringComparer.OrdinalIgnoreCase);

        var missing = preset.Modules.Where(m => !beforeCurrent.ContainsKey(m.Name)).ToList();
        var toActivate = _inactiveModules.Where(m => wanted.Contains(m.Name)).Select(m => m.FullPath).ToList();
        var toDeactivate = _activeModules.Where(m => !wanted.Contains(m.Name)).Select(m => m.FullPath).ToList();

        Cursor = Cursors.WaitCursor;
        if (toActivate.Count > 0) MoveModules(toActivate, toActive: true);
        if (toDeactivate.Count > 0) MoveModules(toDeactivate, toActive: false);

        // Recompute against the CURRENT (post-move) locations. MoveModules() above may have
        // relocated some of these folders, and comparing against the pre-move snapshot's now
        // stale FullPath values would make ComputeFingerprint operate on a path that no longer
        // exists (it fails safe and returns ""), producing a false "this module changed"
        // warning for every module that was just activated/deactivated.
        var afterCurrent = _activeModules.Concat(_inactiveModules)
            .GroupBy(m => m.Name, StringComparer.OrdinalIgnoreCase)
            .ToDictionary(g => g.Key, g => g.First(), StringComparer.OrdinalIgnoreCase);

        // Fingerprint (and therefore this check) is only present for non-futureproof presets --
        // ModuleRef.Fingerprint is left empty for futureproof imports, so this naturally no-ops for those.
        var mismatches = new List<string>();
        foreach (var pm in preset.Modules)
        {
            if (afterCurrent.TryGetValue(pm.Name, out var local) && !string.IsNullOrEmpty(pm.Fingerprint))
            {
                var localFp = ModuleScanner.ComputeFingerprint(local.FullPath);
                if (!string.Equals(localFp, pm.Fingerprint, StringComparison.Ordinal))
                    mismatches.Add($"{pm.Name}  (preset expects v{pm.Version}; your local copy appears different)");
            }
        }
        Cursor = Cursors.Default;

        var msg = new StringBuilder();
        if (missing.Count > 0)
        {
            msg.AppendLine("These modules are in the preset but not installed locally:");
            foreach (var m in missing)
            {
                var versionSuffix = string.IsNullOrEmpty(m.Version) ? "" : $"  (v{m.Version})";
                msg.AppendLine($"   - {m.Name}{versionSuffix}");
            }
            msg.AppendLine();
        }
        if (mismatches.Count > 0)
        {
            msg.AppendLine("These modules appear to have changed since the preset was saved:");
            foreach (var m in mismatches) msg.AppendLine($"   - {m}");
        }

        if (msg.Length > 0)
            ShowScrollableMessage($"Applied Preset: {preset.Name}", msg.ToString());
        else
            lblStatus.Text = $"Applied preset '{preset.Name}'.";
    }

    private void DeletePreset()
    {
        var preset = GetSelectedPreset();
        if (preset == null) return;

        var confirm = MessageBox.Show(this, $"Delete preset '{preset.Name}'?", "Delete Preset",
            MessageBoxButtons.YesNo, MessageBoxIcon.Warning);
        if (confirm != DialogResult.Yes) return;

        _config.Presets.Remove(preset);
        SaveConfig();
        RefreshPresetCombo();
    }

    private void ExportPreset()
    {
        var preset = GetSelectedPreset();
        if (preset == null) return;

        var futureproof = chkFutureproof.Checked;
        var code = PresetCodec.Encode(preset, futureproof, ReadModVersion());
        Clipboard.SetText(code);

        var overLimit = code.Length > PresetCodec.DiscordSafeLimit;
        var warning = overLimit
            ? $"\n\nHeads up: this code is {code.Length} characters, over Discord's 2000-character message limit. " +
              (futureproof ? "Try trimming the preset to fewer modules." : "Try the Futureproof option to shrink it, or trim the preset.")
            : "";

        MessageBox.Show(this,
            $"Preset '{preset.Name}' was copied to your clipboard as a share code ({code.Length} characters).{warning}",
            "Export Preset", MessageBoxButtons.OK, overLimit ? MessageBoxIcon.Warning : MessageBoxIcon.Information);
    }

    private void ImportPreset()
    {
        var text = InputForm.Prompt(this, "Import Preset", "Paste the preset share code:", "", multiline: true);
        if (string.IsNullOrWhiteSpace(text)) return;

        Preset preset;
        try
        {
            preset = PresetCodec.Decode(text ?? "");
        }
        catch (Exception ex)
        {
            MessageBox.Show(this, $"Couldn't read that preset code:\n{ex.Message}", "Import Error",
                MessageBoxButtons.OK, MessageBoxIcon.Error);
            return;
        }

        var name = InputForm.Prompt(this, "Name This Preset", "Save the imported preset as:", preset.Name);
        if (string.IsNullOrWhiteSpace(name)) return;
        preset.Name = name!.Trim();

        var existing = _config.Presets.FirstOrDefault(p => p.Name.Equals(preset.Name, StringComparison.OrdinalIgnoreCase));
        if (existing != null) _config.Presets.Remove(existing);

        _config.Presets.Add(preset);
        SaveConfig();
        RefreshPresetCombo();
        cmbPresets.SelectedItem = preset.Name;

        var localVersion = ReadModVersion();
        var versionNote = (!string.IsNullOrEmpty(preset.SourceVersion) &&
                            !string.Equals(preset.SourceVersion, localVersion, StringComparison.OrdinalIgnoreCase))
            ? $"\n\nNote: this preset was exported from AoE v{preset.SourceVersion}; you're running v{localVersion}."
            : "";

        var apply = MessageBox.Show(this,
            $"Preset '{preset.Name}' imported with {preset.Modules.Count} modules.{versionNote}\n\nApply it now?",
            "Import Preset", MessageBoxButtons.YesNo, MessageBoxIcon.Question);
        if (apply == DialogResult.Yes)
            ApplyPreset(preset);
    }
}
