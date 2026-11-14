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

    /// Resolved fresh from placement validation each run; never persisted or manually overridden.
    private string? _btsExePath;

    private const string LauncherVersion = "1.0";

    /// What a version.txt value must look like to be shown on the Launch button (a short single token such as "380").
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
    private Panel _topPanel = null!;
    private Panel _bottomPanel = null!;
    private Panel _filterPanel = null!;
    private readonly List<TagFilterBox> _filterBoxes = new();
    private readonly ToolTip _filterToolTip = new();

    /// The tags that get a filter box, in display order. Add a name here to add a filter.
    private static readonly string[] FilterTags = { "Civ", "Mech", "Art", "Joke" };
    private Panel _statusPanel = null!;
    private Button btnManage = null!;

    private const int MinFormWidth = 900;
    private const int ExpandedMinHeight = 520;

    /// Client height to restore when the module section is revealed. Starts as the saved (or
    /// default) height, and follows the user's resizing while the module section is shown.
    private int _expandedClientHeight;

    /// True while the code itself is resizing/re-laying-out the window, so those size changes
    /// aren't mistaken for the user resizing it.
    private bool _applyingLayout;

    /// True while the user is dragging the window's edge. Work that only needs to be right once
    /// the drag finishes (re-centering the splitter) is skipped meanwhile and done in OnResizeEnd.
    private bool _userResizing;

    /// Window state as of the last size/state change, used to notice maximize/restore.
    private FormWindowState _lastWindowState = FormWindowState.Normal;

    public MainForm()
    {
        Text = "Ashes of Erebus Launcher";
        Width = 1200;
        Height = 700;
        StartPosition = FormStartPosition.CenterScreen;
        MinimumSize = new Size(MinFormWidth, ExpandedMinHeight);
        _expandedClientHeight = ClientSize.Height;

        // Loaded here rather than in MainForm_Load so the saved Manage Modules state and window
        // size are known before the window is first shown (no visible resize flash on startup).
        _config = ConfigManager.Load();
        RestoreWindowSize();

        DoubleBuffered = true;
        Theme.StyleForm(this);
        //LoadBackgroundImage(); // disabled: WinForms can't layer alpha-blended controls over a background image

        BuildUi();
        SetupDragDrop();
        ApplyModulesVisibility(_config.ModulesVisible, initial: true);

        // Maximizing only applies when the module section is shown (the hidden state has a fixed height).
        if (_config.ModulesVisible && _config.WindowMaximized)
            WindowState = FormWindowState.Maximized;
        _lastWindowState = WindowState;

        Load += MainForm_Load;
    }

    // ------------------------------------------------------- Window size ---

    /// Applies the saved window size (if any), clamped to the current screen so a window saved on
    /// a larger monitor can't open bigger than the display. Only the width and the expanded
    /// height are stored; the collapsed height is derived from the layout.
    private void RestoreWindowSize()
    {
        if (_config.WindowClientWidth <= 0 || _config.WindowClientHeight <= 0)
            return;

        var area = Screen.PrimaryScreen?.WorkingArea ?? new Rectangle(0, 0, 1920, 1080);
        var width = Math.Min(_config.WindowClientWidth, area.Width);
        var height = Math.Min(_config.WindowClientHeight, area.Height - 60); // leave room for the title bar and frame

        _applyingLayout = true;
        ClientSize = new Size(width, height);
        _applyingLayout = false;

        _expandedClientHeight = ClientSize.Height;
    }

    /// Records the window's current size into the in-memory config. Sizes are only taken while
    /// the window is in its normal state; a maximized or minimized window keeps the last normal size.
    private void CaptureWindowSize()
    {
        if (_applyingLayout || WindowState != FormWindowState.Normal) return;

        _config.WindowClientWidth = ClientSize.Width;
        if (_config.ModulesVisible)
        {
            _expandedClientHeight = ClientSize.Height;
            _config.WindowClientHeight = ClientSize.Height;
        }
        else
        {
            _config.WindowClientHeight = _expandedClientHeight;
        }
    }

    protected override void OnSizeChanged(EventArgs e)
    {
        base.OnSizeChanged(e);
        if (_applyingLayout) return;

        CaptureWindowSize();

        // Maximize / restore doesn't raise ResizeEnd, so persist those transitions here.
        if (WindowState != _lastWindowState && WindowState != FormWindowState.Minimized)
        {
            _config.WindowMaximized = WindowState == FormWindowState.Maximized;
            SaveConfig();
        }
        if (WindowState != FormWindowState.Minimized)
            _lastWindowState = WindowState;
    }

    protected override void OnResizeBegin(EventArgs e)
    {
        base.OnResizeBegin(e);
        _userResizing = true;
    }

    /// Fires once when the user finishes dragging the window's edge or title bar (not on every
    /// pixel of the drag): re-centers the splitter and saves the size if it actually changed.
    protected override void OnResizeEnd(EventArgs e)
    {
        base.OnResizeEnd(e);
        _userResizing = false;

        var oldWidth = _config.WindowClientWidth;
        var oldHeight = _config.WindowClientHeight;
        CaptureWindowSize();

        if (_splitContainer.Visible) CenterSplitter();

        if (_config.WindowClientWidth != oldWidth || _config.WindowClientHeight != oldHeight)
            SaveConfig();
    }

    protected override void OnFormClosing(FormClosingEventArgs e)
    {
        base.OnFormClosing(e);
        if (e.Cancel) return;
        CaptureWindowSize();
        if (WindowState != FormWindowState.Minimized)
            _config.WindowMaximized = WindowState == FormWindowState.Maximized;
        SaveConfig();
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
        var topPanel = new BufferedPanel { Dock = DockStyle.Top, Height = 130 };
        Theme.StyleContainer(topPanel);
        _topPanel = topPanel;

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

        var btnCiv4Config = new FlatButton { Text = "Open Civ4 Config", Width = 150, Height = Theme.ButtonHeight, Top = 13 };
        Theme.StyleButton(btnCiv4Config);
        btnCiv4Config.Click += (s, e) => OpenCiv4Config();

        // Toggles the module lists + preset tools; centered on its own row beneath Launch.
        btnManage = new FlatButton { Text = "Manage Modules", Width = 150, Height = Theme.ButtonHeight, Top = 92 };
        Theme.StyleButton(btnManage);
        btnManage.Click += (s, e) =>
        {
            var show = !_config.ModulesVisible;
            ApplyModulesVisibility(show, initial: false);
            _config.ModulesVisible = show;
            SaveConfig();
        };

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
        topPanel.Controls.Add(btnCiv4Config);
        topPanel.Controls.Add(btnManage);
        topPanel.Controls.Add(chkCloseOnLaunch);
        topPanel.Resize += (s, e) =>
        {
            btnLaunch.Left = (topPanel.Width - btnLaunch.Width) / 2;
            btnManage.Left = (topPanel.Width - btnManage.Width) / 2;
            btnCiv4Config.Left = topPanel.Width - btnCiv4Config.Width - 12;
            chkCloseOnLaunch.Left = topPanel.Width - chkCloseOnLaunch.Width - 12;
        };

        _splitContainer = new BufferedSplitContainer
        {
            Dock = DockStyle.Fill,
            Orientation = Orientation.Vertical,
            IsSplitterFixed = true, // panes are always an even 50/50 split -- no draggable divider
            SplitterWidth = 3,
        };
        Theme.StyleContainer(_splitContainer);
        _splitContainer.Resize += (s, e) => CenterSplitter();

        var activeGroup = new BufferedGroupBox { Text = "Active Modules (loaded in-game)", Dock = DockStyle.Fill };
        Theme.StyleContainer(activeGroup);
        dgvActive = CreateModuleGrid();
        activeGroup.Controls.Add(dgvActive);

        var inactiveGroup = new BufferedGroupBox { Text = "Inactive Modules (installed, not loaded)", Dock = DockStyle.Fill };
        Theme.StyleContainer(inactiveGroup);
        dgvInactive = CreateModuleGrid();
        inactiveGroup.Controls.Add(dgvInactive);

        _splitContainer.Panel1.Controls.Add(activeGroup);
        _splitContainer.Panel2.Controls.Add(inactiveGroup);

        // Tag filter row, centered between the module lists and the preset tools.
        var filterPanel = new BufferedPanel { Dock = DockStyle.Bottom, Height = 32 };
        Theme.StyleContainer(filterPanel);
        _filterPanel = filterPanel;

        var lblFilters = new Label { Text = "Filters:", AutoSize = false, TextAlign = ContentAlignment.MiddleLeft, Height = 22 };
        lblFilters.Width = TextRenderer.MeasureText(lblFilters.Text, lblFilters.Font).Width + 4;
        Theme.StyleLabel(lblFilters);
        filterPanel.Controls.Add(lblFilters);

        _filterToolTip.SetToolTip(lblFilters,
            "Click a tag's box to cycle it: empty = no filter, white = only show modules WITH the tag, " +
            "black = grey out modules WITH the tag. Right-click a box to clear it.\n" +
            "Greyed-out modules are moved to the bottom of their list but are still active/inactive as before.");
        foreach (var tag in FilterTags)
        {
            var box = new TagFilterBox { Text = tag };
            box.FitToText();
            box.StateChanged += (s, e) => OnFilterChanged();
            _filterToolTip.SetToolTip(box,
                $"{tag}: click to cycle (empty = no filter, white = only {tag} modules, black = hide {tag} modules). Right-click to clear.");
            _filterBoxes.Add(box);
            filterPanel.Controls.Add(box);
        }

        void LayoutFilterRow()
        {
            const int spacing = 20;
            var items = new List<Control> { lblFilters };
            items.AddRange(_filterBoxes);
            var total = items.Sum(c => c.Width) + spacing * (items.Count - 1);
            var x = Math.Max(0, (filterPanel.Width - total) / 2);
            foreach (var c in items)
            {
                c.Left = x;
                c.Top = (filterPanel.Height - c.Height) / 2;
                x += c.Width + spacing;
            }
        }
        filterPanel.Resize += (s, e) => LayoutFilterRow();
        LayoutFilterRow();

        var bottomPanel = new BufferedPanel { Dock = DockStyle.Bottom, Height = 88 };
        Theme.StyleContainer(bottomPanel);
        _bottomPanel = bottomPanel;

        // Row 1: preset save/load/delete, with the dev action right-aligned on the same line
        var btnSave = new FlatButton { Text = "Save Active Modules As New Preset", Left = 12, Top = 8, Width = 250, Height = Theme.ButtonHeight };
        cmbPresets = new ComboBox { Left = 270, Top = 11, Width = 170, DropDownStyle = ComboBoxStyle.DropDownList };
        var btnLoad = new FlatButton { Text = "Load Preset", Left = 448, Top = 8, Width = 110, Height = Theme.ButtonHeight };
        var btnDelete = new FlatButton { Text = "Delete", Left = 566, Top = 8, Width = 80, Height = Theme.ButtonHeight };
        var btnRefresh = new FlatButton { Text = "Refresh", Top = 8, Width = 90, Height = Theme.ButtonHeight };
        Theme.StyleButton(btnSave);
        Theme.StyleComboBox(cmbPresets);
        Theme.StyleButton(btnLoad);
        Theme.StyleButton(btnDelete);
        Theme.StyleButton(btnRefresh);
        btnRefresh.Click += (s, e) => RefreshModules();

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
            btnSave, cmbPresets, btnLoad, btnDelete, btnRefresh, btnImport, btnExport, chkFutureproof, btnDevSchemas
        });
        bottomPanel.Resize += (s, e) => { btnRefresh.Left = bottomPanel.Width - btnRefresh.Width - 12; };
        bottomPanel.Resize += (s, e) => { btnDevSchemas.Left = bottomPanel.Width - btnDevSchemas.Width - 12; };

        // Status bar: status text fills the left, launcher version sits at the right.
        var statusPanel = new BufferedPanel { Dock = DockStyle.Bottom, Height = 26 };
        Theme.StyleContainer(statusPanel);
        _statusPanel = statusPanel;

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

        // Dock order: later-added edge panels sit further from the Fill control, so the filter row
        // goes in before the bottom panel to sit directly under the module lists.
        Controls.Add(_splitContainer);
        Controls.Add(filterPanel);
        Controls.Add(bottomPanel);
        Controls.Add(statusPanel);
        Controls.Add(topPanel);
    }

    /// Shows or hides everything beneath the Manage Modules button (the module lists and the
    /// preset/dev tools -- the status bar stays), swaps the button's text, and resizes the window:
    /// shrunk to just the top section + status bar when hidden (with the height locked, since
    /// there's nothing to gain from a taller window), and restored to its expanded height when shown.
    private void ApplyModulesVisibility(bool show, bool initial)
    {
        _applyingLayout = true;
        SuspendLayout();

        if (show)
        {
            MaximumSize = Size.Empty;
            MinimumSize = new Size(MinFormWidth, ExpandedMinHeight);
            MaximizeBox = true;
            _splitContainer.Visible = true;
            _bottomPanel.Visible = true;
            _filterPanel.Visible = true;
            ClientSize = new Size(ClientSize.Width, _expandedClientHeight);
        }
        else
        {
            // A maximized window can't be shrunk; restore it first so the size math below applies.
            if (!initial && WindowState != FormWindowState.Normal)
            {
                WindowState = FormWindowState.Normal;
                _lastWindowState = FormWindowState.Normal;
                _config.WindowMaximized = false;
            }
            if (!initial)
            {
                _expandedClientHeight = ClientSize.Height;
                _config.WindowClientHeight = _expandedClientHeight;
                _config.WindowClientWidth = ClientSize.Width;
            }

            _splitContainer.Visible = false;
            _bottomPanel.Visible = false;
            _filterPanel.Visible = false;
            MaximizeBox = false;
            ApplyCollapsedSize();
        }

        btnManage.Text = show ? "Hide Modules" : "Manage Modules";
        ResumeLayout(true);
        _applyingLayout = false;

        // If expanding pushed the bottom edge off-screen, slide the window up to fit.
        if (show && !initial && IsHandleCreated)
        {
            var wa = Screen.FromControl(this).WorkingArea;
            if (Bottom > wa.Bottom)
                Top = Math.Max(wa.Top, wa.Bottom - Height);
        }
    }

    /// Sizes the window to just the top section + status bar and pins its height there (width
    /// stays freely resizable). Safe to call repeatedly; also re-run once the window handle exists
    /// so the pinned height matches the real, as-created non-client area.
    private void ApplyCollapsedSize()
    {
        MaximumSize = Size.Empty;
        MinimumSize = new Size(MinFormWidth, 0);
        ClientSize = new Size(ClientSize.Width, _topPanel.Height + _statusPanel.Height);
        MinimumSize = new Size(MinFormWidth, Height);
        MaximumSize = new Size(SystemInformation.VirtualScreen.Width, Height);
    }

    /// Keeps the two panes an even 50/50 split. When the window is minimized (or otherwise
    /// squeezed very small) the container's width can drop below Panel1MinSize + Panel2MinSize +
    /// SplitterWidth, at which point NO SplitterDistance is valid and assigning one throws. In
    /// that case there's nothing sensible to do, so leave it alone; the container fires Resize
    /// again on restore and the split is re-centered then.
    private void CenterSplitter()
    {
        // During an edge drag the container already scales the splitter proportionally; forcing an
        // exact re-center on every resize event just adds a relayout of both grids per mouse move.
        // OnResizeEnd re-centers once the drag is over.
        if (_userResizing) return;

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
            ShowCellToolTips = false, // ModuleGridView draws its own tooltips (see ModuleGridView)
        };
        Theme.StyleGrid(grid);

        var nameCol = new DataGridViewTextBoxColumn
        {
            Name = "Name", HeaderText = "Module",
            AutoSizeMode = DataGridViewAutoSizeColumnMode.Fill,
            Resizable = DataGridViewTriState.False,
        };

        // Fixed-width, non-resizable text column; centered ones also center their header.
        static DataGridViewTextBoxColumn FixedCol(string name, string header, int width, bool centered = false)
        {
            var col = new DataGridViewTextBoxColumn
            {
                Name = name, HeaderText = header,
                AutoSizeMode = DataGridViewAutoSizeColumnMode.None,
                Width = width,
                Resizable = DataGridViewTriState.False,
            };
            if (centered)
            {
                col.DefaultCellStyle.Alignment = DataGridViewContentAlignment.MiddleCenter;
                col.HeaderCell.Style.Alignment = DataGridViewContentAlignment.MiddleCenter;
            }
            return col;
        }

        var infoCol = new DataGridViewButtonColumn
        {
            Name = "Info",
            HeaderText = "Info",
            AutoSizeMode = DataGridViewAutoSizeColumnMode.None,
            Width = 32,
            Resizable = DataGridViewTriState.False,
            FlatStyle = FlatStyle.Flat,
        };

        // Module | Version | AoE Rev | Loadpass | Info
        grid.Columns.AddRange(
            nameCol,
            FixedCol("Version", "Version", 64),
            FixedCol("AoERev", "AoE Rev", 66),
            FixedCol("LoadPass", "Loadpass", 70, centered: true),
            infoCol);
        return grid;
    }

    // ---------------------------------------------------------- Lifecycle ---

    private void MainForm_Load(object? sender, EventArgs e)
    {
        // _config was already loaded in the constructor (the saved Manage Modules state is needed
        // before the window is shown).
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

        // Now that the window handle exists, re-pin the collapsed height against the real frame size.
        if (!_config.ModulesVisible)
            ApplyCollapsedSize();

        RefreshModules(true);
        RefreshPresetCombo();
    }

    /// Returns true if the app should proceed, false if the user chose to quit.
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

    /// Sets the Launch button text: "not found" when the game executable can't be located,
    /// otherwise the version from version.txt, or "v?" if that file is missing or malformed.
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

        if (!VerifyActiveModules("launching the game"))
        {
            lblStatus.Text = "Launch aborted.";
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

    // ------------------------------------------------------- Verification ---

    /// Checks the currently active modules (freshly scanned, so manual changes on disk since the
    /// last refresh are included). Returns true if everything is fine or the user chose to continue.
    private bool VerifyActiveModules(string action)
    {
        var installed = ModuleScanner.ScanAll(_modPath);
        var set = installed.Where(m => m.IsActive).Select(m => new LoadEntry(m, m.LoadPass)).ToList();
        return VerifyModuleSet(action, set, installed, "active");
    }

    /// Checks the modules of a preset as the preset would load them (using the load passes it
    /// records). Modules the preset names but that aren't installed locally can't be checked
    /// and are skipped.
    private bool VerifyPresetModules(Preset preset, string action)
    {
        var installed = ModuleScanner.ScanAll(_modPath);
        var set = new List<LoadEntry>();
        foreach (var pm in preset.Modules)
        {
            var local = installed
                .Where(m => string.Equals(m.FolderName, pm.Name, StringComparison.OrdinalIgnoreCase))
                .OrderByDescending(m => m.IsActive)
                .FirstOrDefault();
            if (local != null) set.Add(new LoadEntry(local, pm.LoadPass));
        }
        return VerifyModuleSet(action, set, installed, "in the preset");
    }

    /// Runs the incompatibility check, then the dependency check, each with its own
    /// abort/continue popup. Returns false as soon as the user aborts.
    /// `setDescription` completes "...is not ___" / "...both ___" in the messages.
    private bool VerifyModuleSet(string action, List<LoadEntry> set, List<ModuleInfo> installed, string setDescription)
    {
        var incompatible = ModuleChecker.CheckIncompatibilities(set);
        if (incompatible.Count > 0)
        {
            var text = new StringBuilder();
            text.AppendLine($"These modules are marked as incompatible with each other, but both are {setDescription}:");
            text.AppendLine();
            foreach (var issue in incompatible) text.AppendLine($"   - {issue}");
            text.AppendLine();
            text.AppendLine($"Continue anyway, or abort {action}?");

            if (!ShowConfirmMessage("Incompatible Modules", text.ToString(), "Continue", "Abort", cancelIsDefault: true))
                return false;
        }

        var dependencies = ModuleChecker.CheckDependencies(set, installed, setDescription);
        if (dependencies.Count > 0)
        {
            var text = new StringBuilder();
            text.AppendLine("Some modules have dependencies that won't be loaded before them. A dependency must be " +
                            "present and load earlier: pass Default first, then 1, 2, 3, 4, and alphabetically by folder " +
                            "name within a pass.");
            text.AppendLine();
            foreach (var issue in dependencies)
            {
                text.AppendLine(issue);
                text.AppendLine();
            }
            text.AppendLine($"Continue anyway, or abort {action}?");

            if (!ShowConfirmMessage("Module Dependencies", text.ToString(), "Continue", "Abort", cancelIsDefault: true))
                return false;
        }

        return true;
    }

    // ------------------------------------------------------------ Modules ---

    private void RefreshModules(bool firstLaunch = false)
    {
        Cursor = Cursors.WaitCursor;
        lblStatus.Text = "Scanning modules...";
        UpdateLaunchButtonText();

        var all = ModuleScanner.ScanAll(_modPath);
        _activeModules = all.Where(m => m.IsActive)
            .OrderBy(m => m.Name, StringComparer.OrdinalIgnoreCase).ThenBy(m => m.FolderName, StringComparer.OrdinalIgnoreCase).ToList();
        _inactiveModules = all.Where(m => !m.IsActive)
            .OrderBy(m => m.Name, StringComparer.OrdinalIgnoreCase).ThenBy(m => m.FolderName, StringComparer.OrdinalIgnoreCase).ToList();

        RepopulateGrids(keepScroll: true);

        if (firstLaunch)
            lblStatus.Text = $"Welcome to the launcher! First time users may find the \"Instructions\" button useful.";
        else
            lblStatus.Text = CountStatusText();

        Cursor = Cursors.Default;
    }

    /// Redraws both lists from the already-scanned modules, preserving selection (and, optionally,
    /// scroll position), with filtered-out modules greyed and sorted to the bottom.
    private void RepopulateGrids(bool keepScroll)
    {
        var activeScroll = keepScroll ? SafeScrollIndex(dgvActive) : 0;
        var inactiveScroll = keepScroll ? SafeScrollIndex(dgvInactive) : 0;
        var activeSelected = SelectedNames(dgvActive);
        var inactiveSelected = SelectedNames(dgvInactive);

        PopulateGrid(dgvActive, _activeModules, activeSelected, activeScroll);
        PopulateGrid(dgvInactive, _inactiveModules, inactiveSelected, inactiveScroll);
    }

    private bool AnyFilterActive => _filterBoxes.Any(b => b.State != TagFilterState.Neutral);

    /// True if the module doesn't pass the tag filters: it lacks a whitelisted tag (every
    /// whitelisted tag is required) or has a blacklisted one.
    private bool IsFilteredOut(ModuleInfo m)
    {
        foreach (var box in _filterBoxes)
        {
            var has = m.Tags.Contains(box.Text);
            if (box.State == TagFilterState.Whitelist && !has) return true;
            if (box.State == TagFilterState.Blacklist && has) return true;
        }
        return false;
    }

    private string CountStatusText()
    {
        var text = $"{_activeModules.Count} active, {_inactiveModules.Count} inactive modules.";
        if (AnyFilterActive)
        {
            var a = _activeModules.Count(IsFilteredOut);
            var i = _inactiveModules.Count(IsFilteredOut);
            text += $"  Filters on: {a} active and {i} inactive greyed out.";
        }
        return text;
    }

    private void OnFilterChanged()
    {
        RepopulateGrids(keepScroll: false);
        lblStatus.Text = CountStatusText();
    }

    private static int SafeScrollIndex(DataGridView grid) =>
        grid.Rows.Count > 0 ? grid.FirstDisplayedScrollingRowIndex : 0;

    private static HashSet<string> SelectedNames(DataGridView grid) =>
        new(grid.SelectedRows.Cast<DataGridViewRow>().Select(r => ((ModuleInfo)r.Tag!).FolderName), StringComparer.OrdinalIgnoreCase);

    /// Repopulates a grid while preserving scroll position and selection where possible (both otherwise
    /// reset on Rows.Clear()). Modules failing the tag filters are listed after the others, greyed out;
    /// the sort is stable, so each group stays in name order.
    private void PopulateGrid(DataGridView grid, List<ModuleInfo> modules, HashSet<string> selectedNames, int scrollIndex)
    {
        grid.Rows.Clear();
        foreach (var m in modules.OrderBy(m => IsFilteredOut(m) ? 1 : 0))
        {
            var infoText = !string.IsNullOrWhiteSpace(m.Desc) ? "i" : "";
            // Values must follow the column order set up in CreateModuleGrid.
            var idx = grid.Rows.Add(
                m.Name,
                m.Version, m.AoeRev, ModuleLayout.PassDisplayName(m.LoadPass),
                infoText);
            var row = grid.Rows[idx];
            row.Tag = m;
            if (IsFilteredOut(m))
            {
                row.DefaultCellStyle.ForeColor = Theme.FilteredText;
                row.DefaultCellStyle.SelectionForeColor = Theme.FilteredSelectionText;
                row.DefaultCellStyle.SelectionBackColor = Theme.FilteredSelectionBack;
            }
            if (!string.IsNullOrWhiteSpace(m.ShortDesc))
            {
                foreach (DataGridViewCell cell in row.Cells)
                    if (grid.Columns[cell.ColumnIndex].Name != "Info")
                        cell.ToolTipText = m.ShortDesc;
            }
            // Explicitly set true/false (not just conditionally true): DataGridView can
            // auto-select the first row as a side effect of adding rows/assigning the
            // current cell, and leaving that implicit rather than overriding it here caused
            // the top row to end up selected after every refresh even when nothing should be.
            row.Selected = selectedNames.Contains(m.FolderName);
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
        if (!string.IsNullOrWhiteSpace(m.AoeRev)) text.AppendLine($"AoE Rev: {m.AoeRev}");
        text.AppendLine($"Load pass: {ModuleLayout.PassDisplayName(m.LoadPass)}");
        if (!string.Equals(m.Name, m.FolderName, StringComparison.Ordinal)) text.AppendLine($"Folder: {m.FolderName}");
        if (!string.IsNullOrWhiteSpace(m.Author)) text.AppendLine($"Author: {m.Author}");
        if (m.Compatible.Count > 0) text.AppendLine($"Compatible with: {string.Join(", ", m.Compatible)}");
        if (m.Dependencies.Count > 0) text.AppendLine($"Requires: {string.Join(", ", m.Dependencies)}");
        if (m.Incompatible.Count > 0) text.AppendLine($"Incompatible with: {string.Join(", ", m.Incompatible)}");
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
- The Manage Modules button shows or hides the module lists and preset tools; the launcher remembers your choice

    USING MODULES
- Changing the status of a module simply makes this launcher move the game files for you; it can be done manually
- You can either doubleclick a module to move which side it is on, or click and drag it across
- Shift clicking a module with one already selected will select it and all modules between the two
- Control-clicking a module will toggle the selection of that specific module
- The Refresh button will update the shown module list if you manually move files with the launcher open
- The Filters row greys out modules by tag (from each module's info.txt): click a tag's box to cycle it between empty (no filter), white (only show modules WITH that tag) and black (grey out modules WITH that tag); right-click clears it
- Greyed-out modules move to the bottom of their list but are NOT removed: they stay active or inactive exactly as before, so check your filters before launching
- Right-click a module and choose ""Load in pass"" to move it between the Default folder (Def) and the sequenced passes 1-4 (Seq); the Loadpass column shows where each module currently is
- The game loads Default modules first, then pass 1, 2, 3 and 4; within each pass modules load alphabetically by their folder name
- Moving a module between active and inactive keeps its load pass
- Before launching, saving a preset or exporting a preset, the launcher checks that no active modules are listed as incompatible with each other, and that every module's dependencies are active and load before it; you can abort or continue if a problem is found

    PRESETS
- Pressing the ""Save..."" button will give you the option to save the current selection as a preset
- Pressing the Load Preset button will cause the currently selected preset in the dropdown box to be loaded
- Presets remember each module's load pass, and loading one puts modules back in those passes
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

    /// Normalizes any mix of bare \n, bare \r, or \r\n line endings to Environment.NewLine.
    /// ReadOnlySelectableTextBox wraps a RichTextBox (the usual way to get read-only,
    /// *selectable* text, since a plain Label can't be selected) -- and RichTextBox silently
    /// drops line breaks that are a bare \n with no \r. That's exactly what text coming from a
    /// module's Desc field tends to be, since it's often authored/edited on a non-Windows
    /// machine. Routing every string through here before it reaches the box, rather than
    /// patching individual call sites, is what actually fixes that for good.
    private static string NormalizeNewlines(string text) =>
        text.Replace("\r\n", "\n").Replace("\r", "\n").Replace("\n", Environment.NewLine);

    /// Generic scrollable read-only message dialog, styled to match the app, with a single OK button.
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

    /// Same as ShowScrollableMessage but with Apply/Cancel, returning true if the user confirmed.
    private bool ShowConfirmMessage(string title, string text, string confirmText = "Apply", string cancelText = "Cancel",
        bool cancelIsDefault = false)
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
        form.AcceptButton = cancelIsDefault ? cancelBtn : confirmBtn;
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
        contextMenu.Items.Add(new ToolStripSeparator());

        // The module(s) the "Load in pass" items act on, captured when the menu opens: the whole
        // selection if the right-clicked row is part of it, otherwise just the right-clicked row.
        var contextTargets = new List<ModuleInfo>();
        var passItems = new List<ToolStripMenuItem>();
        foreach (var pass in ModuleLayout.Passes)
        {
            var targetPass = pass;
            var item = new ToolStripMenuItem($"Load in pass: {ModuleLayout.PassDisplayName(targetPass)}") { Tag = targetPass };
            item.Click += (s, e) =>
            {
                var requests = contextTargets
                    .Select(m => new MoveRequest { Source = m.FullPath, ToActive = m.IsActive, Pass = targetPass })
                    .ToList();
                if (requests.Count > 0) PerformMoves(requests);
            };
            contextMenu.Items.Add(item);
            passItems.Add(item);
        }

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
            {
                e.Cancel = true;
                return;
            }

            contextTargets = GetContextTargets(grid, contextRowIndex);

            // Hide the pass the module(s) are already in. With a multi-selection spanning several
            // passes an option stays visible as long as it would move at least one of them.
            foreach (var item in passItems)
            {
                var pass = (string)item.Tag!;
                item.Visible = contextTargets.Any(m => !string.Equals(m.LoadPass, pass, StringComparison.Ordinal));
            }
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

    /// Opens the Civ4 config .ini via the shortcut two levels above the mod folder
    /// (..\..\_Civ4Config, i.e. next to Civ4BeyondSword.exe). The shell follows the shortcut and
    /// opens its target with the user's default program for .ini files, so there's no need to
    /// resolve the .lnk ourselves. Tries "_Civ4Config.lnk" first, then a bare "_Civ4Config" in case
    /// it's a differently-made link or the file itself.
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

    /// One module folder to move: where it is, which side it's going to, and into which load pass.
    private sealed class MoveRequest
    {
        public string Source { get; set; } = "";
        public bool ToActive { get; set; }

        /// Target load pass ("Def", "1".."4"); empty/invalid keeps the pass the module is already in.
        public string Pass { get; set; } = "";
    }

    private static List<ModuleInfo> GetContextTargets(DataGridView grid, int rowIndex)
    {
        var clicked = grid.Rows[rowIndex];
        if (clicked.Selected && grid.SelectedRows.Count > 1)
        {
            return grid.SelectedRows.Cast<DataGridViewRow>()
                .Select(r => r.Tag).OfType<ModuleInfo>().ToList();
        }
        return clicked.Tag is ModuleInfo m ? new List<ModuleInfo> { m } : new List<ModuleInfo>();
    }

    private static bool SamePath(string a, string b) =>
        string.Equals(Path.GetFullPath(a).TrimEnd('\\'), Path.GetFullPath(b).TrimEnd('\\'), StringComparison.OrdinalIgnoreCase);

    /// Moves modules between the active/inactive sides, keeping each one's load pass.
    private void MoveModules(List<string> sourcePaths, bool toActive)
    {
        PerformMoves(sourcePaths
            .Select(p => new MoveRequest { Source = p, ToActive = toActive, Pass = "" })
            .ToList());
    }

    /// Performs every requested move (between sides and/or between load passes), reports any
    /// failures together in one message, and refreshes the lists once at the end.
    private void PerformMoves(List<MoveRequest> requests)
    {
        var errors = new List<string>();
        foreach (var req in requests)
        {
            try
            {
                var src = req.Source.TrimEnd(Path.DirectorySeparatorChar, Path.AltDirectorySeparatorChar);
                var name = Path.GetFileName(src);

                // An unspecified pass keeps the module in the pass it's already in, which is what
                // preserves the Def / Seq\N structure when toggling active <-> inactive.
                var pass = ModuleLayout.NormalizePass(req.Pass);
                if (pass.Length == 0) pass = ModuleLayout.GetPassFromPath(src);

                var targetDir = ModuleLayout.GetPassDir(_modPath, req.ToActive, pass);
                var dest = Path.Combine(targetDir, name);

                if (SamePath(src, dest))
                    continue; // already there

                // A module name must be unique across ALL passes on the destination side, not just
                // the target folder -- otherwise the same module would end up loaded twice.
                var clash = ModuleLayout.FindOnSide(_modPath, req.ToActive, name)
                    .FirstOrDefault(p => !SamePath(p, src));
                if (clash != null)
                {
                    errors.Add($"{name}: a module with this name already exists in the " +
                               $"{(req.ToActive ? "active" : "inactive")} list (load pass {ModuleLayout.PassDisplayName(ModuleLayout.GetPassFromPath(clash))}).");
                    continue;
                }

                Directory.CreateDirectory(targetDir);
                Directory.Move(src, dest);
            }
            catch (Exception ex)
            {
                errors.Add($"{Path.GetFileName(req.Source)}: {ex.Message}");
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
        // Modules dropped in from Explorer carry no pass information, so they go in Def (Default);
        // right-click > Load in pass afterwards if they belong elsewhere.
        var targetDir = ModuleLayout.GetPassDir(_modPath, toActive, ModuleLayout.DefaultPass);
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

                if (ModuleLayout.FindOnSide(_modPath, toActive, name).Count > 0)
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
        if (!VerifyActiveModules("saving the preset"))
            return;

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
                Name = m.FolderName,
                Version = m.Version,
                Fingerprint = ModuleScanner.ComputeFingerprint(m.FullPath),
                LoadPass = m.LoadPass,
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
        var wanted = preset.Modules
            .GroupBy(m => m.Name, StringComparer.OrdinalIgnoreCase)
            .ToDictionary(g => g.Key, g => g.First(), StringComparer.OrdinalIgnoreCase);

        var beforeCurrent = _activeModules.Concat(_inactiveModules)
            .GroupBy(m => m.FolderName, StringComparer.OrdinalIgnoreCase)
            .ToDictionary(g => g.Key, g => g.First(), StringComparer.OrdinalIgnoreCase);

        var missing = preset.Modules.Where(m => !beforeCurrent.ContainsKey(m.Name)).ToList();

        // Wanted modules end up active in the pass the preset recorded (a module with no recorded
        // pass stays in its current pass); unwanted active modules are deactivated, keeping their pass.
        var requests = new List<MoveRequest>();
        foreach (var m in _inactiveModules)
        {
            if (wanted.TryGetValue(m.FolderName, out var pm))
                requests.Add(new MoveRequest { Source = m.FullPath, ToActive = true, Pass = pm.LoadPass });
        }
        foreach (var m in _activeModules)
        {
            if (wanted.TryGetValue(m.FolderName, out var pm))
            {
                var wantedPass = ModuleLayout.NormalizePass(pm.LoadPass);
                if (wantedPass.Length > 0 && !string.Equals(wantedPass, m.LoadPass, StringComparison.Ordinal))
                    requests.Add(new MoveRequest { Source = m.FullPath, ToActive = true, Pass = wantedPass });
            }
            else
            {
                requests.Add(new MoveRequest { Source = m.FullPath, ToActive = false, Pass = "" });
            }
        }

        Cursor = Cursors.WaitCursor;
        if (requests.Count > 0) PerformMoves(requests);

        // Recompute against the CURRENT (post-move) locations. PerformMoves() above may have
        // relocated some of these folders, and comparing against the pre-move snapshot's now
        // stale FullPath values would make ComputeFingerprint operate on a path that no longer
        // exists (it fails safe and returns ""), producing a false "this module changed"
        // warning for every module that was just activated/deactivated.
        var afterCurrent = _activeModules.Concat(_inactiveModules)
            .GroupBy(m => m.FolderName, StringComparer.OrdinalIgnoreCase)
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
                    mismatches.Add($"{local.Name}  (preset expects v{pm.Version}; your local copy appears different)");
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

        if (!VerifyPresetModules(preset, "exporting the preset"))
            return;

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
