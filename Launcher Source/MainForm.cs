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

    private const string LauncherVersion = "1.1";

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
    private StatusIndicator _statusIndicator = null!;
    private readonly ToolTip _statusToolTip = CreateStatusToolTip();

    /// Text of the startup placement problems the user chose to continue past (the same text the
    /// setup-check popup showed); null when the placement check passed. Drives "Install Error".
    private string? _installIssueText;

    private const string GameNotFoundText =
        "The game location couldn't be found. This usually means the mod folder isn't placed correctly! " +
        "Restart the launcher to re-run the setup check.";

    /// Every value the status indicator can show; the control is sized to fit the widest.
    private static readonly string[] StatusValues = { "Ready", "Launched", "Install Error", "Module Issue", "Bad Order" };

    /// Whether Civ4BeyondSword.exe was running the last time it was checked. It is only checked in
    /// response to the user interacting with the launcher (window activated, status hovered, modules
    /// refreshed, game launched), never on a timer.
    private bool _gameRunning;
    private DateTime _lastGameCheckUtc = DateTime.MinValue;
    private static readonly TimeSpan GameCheckThrottle = TimeSpan.FromSeconds(1);

    /// Status tooltips are cut to this many lines so a long problem list can't run off the screen.
    private const int MaxStatusTipLines = 28;
    private Panel _topPanel = null!;
    private Panel _bottomPanel = null!;
    private Panel _filterPanel = null!;
    private Button btnDeletePreset = null!;
    private Button btnLoadPreset = null!;

    /// Holds the filter row (top) and the preset rows (below it) as one block, positioned by hand
    /// rather than by dock order, so the two can never swap places.
    private Panel _bottomStack = null!;
    private readonly List<TagFilterBox> _filterBoxes = new();
    private readonly ToolTip _filterToolTip = CreateStyledToolTip();

    private static ToolTip CreateStyledToolTip()
    {
        var tip = new ToolTip();
        Theme.StyleToolTip(tip);
        return tip;
    }

    /// The status tooltip carries the same text as the popups, so it can be long: wider, quicker to
    /// appear, and kept up for as long as the system allows.
    private static ToolTip CreateStatusToolTip()
    {
        var tip = new ToolTip { InitialDelay = 250, AutoPopDelay = 32000, ReshowDelay = 100 };
        Theme.StyleToolTip(tip, Theme.S(520));
        return tip;
    }

    /// The tags that get a filter box, in display order: the tag exactly as written in info.txt's
    /// [tags] entry, and the label shown to the user. Add a pair here to add a filter.
    private static readonly (string Tag, string Label)[] FilterTags =
    {
        ("Civ(N)", "Civ (New)"), ("Civ(E)", "Civ (Edit)"), ("Art", "Art"), ("Joke", "Joke"),
        ("Mech", "Mechanics"), ("Lead", "Leader"), ("Bal", "Balance"), ("Event", "Event"),
    };

    /// Height of the filter section: heading row, filter box row, and room for the separator line.
    private static readonly int FilterPanelHeight = Theme.S(62);
    private Panel _statusPanel = null!;
    private Button btnManage = null!;

    private const string FutureproofText = "Futureproof";
    private const string FutureproofTip =
        "Futureproof (applies to both Save and Export): leaves each module's version and content " +
        "fingerprint out of the saved preset or exported code. Loading or importing it then only checks " +
        "that each module is installed, with no \"this module looks different\" warnings. The module list " +
        "and each module's Load # are always included either way.";

    private const string SaveButtonText = "Save Active Modules As New Preset";
    private const string ExportButtonText = "Export Active Modules As Preset";

    /// A button just wide enough for its text: the text plus 12 px of padding either side.
    private static int FitButtonWidth(string text) =>
        TextRenderer.MeasureText(text, Theme.BodyFont, Size.Empty, TextFormatFlags.NoPadding | TextFormatFlags.SingleLine).Width
        + Theme.S(24);

    private static readonly int HelpButtonWidth = FitButtonWidth("Instructions");
    private static readonly int ConfigButtonWidth = FitButtonWidth("Open Civ4 Config");
    private static readonly int RefreshButtonWidth = FitButtonWidth("Refresh");
    private static readonly int SchemasButtonWidth = FitButtonWidth("Dev: Update Schemas");

    /// Width shared by the Save and Export buttons so they line up vertically: that of the longer label.
    private static readonly int PresetButtonWidth = Math.Max(FitButtonWidth(SaveButtonText), FitButtonWidth(ExportButtonText));

    /// The checkbox's left edge in the bottom panel: just right of the Save/Export column.
    private static readonly int FutureproofLeftPx = Theme.S(12) + PresetButtonWidth + Theme.S(8);

    private readonly ToolTip _presetToolTip = CreateStyledToolTip();

    /// Longest allowed preset name; the dropdown is sized to show a name of this length.
    private const int MaxPresetNameLength = 24;

    private static readonly int PresetComboWidth =
        TextRenderer.MeasureText(new string('n', MaxPresetNameLength), Theme.BodyFont, Size.Empty,
            TextFormatFlags.NoPadding | TextFormatFlags.SingleLine).Width
        + SystemInformation.VerticalScrollBarWidth + Theme.S(12);

    private static readonly int PresetSideButtonWidth = Theme.S(125); // Delete "<preset>" and Load "<preset>"
    private static readonly int PresetImportButtonWidth = Theme.S(125);

    /// Width of the centered Delete | dropdown | Load group in the first preset row.
    private static readonly int PresetGroupWidth =
        PresetSideButtonWidth + Theme.S(8) + PresetComboWidth + Theme.S(8) + PresetSideButtonWidth;

    /// Heading font of the "Filters:" / "Presets:" rows.
    private const float SectionHeadingScale = 1.15f;

    /// Where the first row of preset buttons starts in the preset panel: below the "Presets:" heading.
    private static readonly int PresetRowsTop =
        Theme.S(4) + Theme.HeadingFont(SectionHeadingScale).Height + Theme.S(4) + Theme.S(6);

    private static readonly int PresetPanelHeight = PresetRowsTop + Theme.ButtonHeight + Theme.S(8) + Theme.ButtonHeight + Theme.S(8);

    /// Checkbox width sized from its text (plus the box glyph), not a hardcoded value.
    private static readonly int FutureproofWidth =
        TextRenderer.MeasureText(FutureproofText, Theme.BodyFont).Width + Theme.S(28);

    /// Width of the filter row: every box plus the gaps between them (mirrors TagFilterBox.FitToText).
    private static readonly int FilterRowWidth =
        FilterTags.Sum(t => TextRenderer.MeasureText(t.Label, Theme.BodyFont, Size.Empty,
                TextFormatFlags.NoPadding | TextFormatFlags.SingleLine).Width + Theme.S(4) + Theme.S(14) + 2)
        + Theme.S(24) * (FilterTags.Length - 1);

    /// The narrowest window at which nothing overlaps, worked out from the actual button widths.
    /// Each line is the width one pair of neighbours needs (W = window width, G = the centered
    /// Delete | dropdown | Load group, C = the dropdown); S(24) allows for the window frame.
    private static readonly int MinFormWidth = new[]
    {
        // top row: Instructions / Open Civ4 Config either side of the 440-wide Launch button
        Theme.S(440) + 2 * (Theme.S(12) + Math.Max(HelpButtonWidth, ConfigButtonWidth) + Theme.S(8)),
        // the centered group stays clear of the Save button on its left...
        2 * FutureproofLeftPx + PresetGroupWidth,
        // ...and of the Refresh button on its right
        PresetGroupWidth + 2 * (Theme.S(12) + RefreshButtonWidth + Theme.S(8)),
        // second row: the Futureproof checkbox stays clear of Import (centered under the dropdown)
        2 * (FutureproofLeftPx + FutureproofWidth + Theme.S(8)
             - (PresetSideButtonWidth + Theme.S(8) + (PresetComboWidth - PresetImportButtonWidth) / 2)) + PresetGroupWidth,
        // ...and Import stays clear of the Dev button on the right
        2 * (PresetSideButtonWidth + Theme.S(8) + (PresetComboWidth + PresetImportButtonWidth) / 2
             + Theme.S(12) + SchemasButtonWidth + Theme.S(8)) - PresetGroupWidth,
        // the filter row
        FilterRowWidth + 2 * Theme.S(12),
    }.Max() + Theme.S(24);
    private static readonly int ExpandedMinHeight = Theme.S(480) + (PresetPanelHeight - (Theme.S(8) + Theme.ButtonHeight + Theme.S(8) + Theme.ButtonHeight + Theme.S(8)));

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
        AutoScaleMode = AutoScaleMode.None;
        Font = Theme.BodyFont; // set first: everything built later inherits it, and measurements below depend on it
        var screenArea = Screen.PrimaryScreen?.WorkingArea ?? new Rectangle(0, 0, 1920, 1080);
        Width = Math.Min(Theme.S(1200), screenArea.Width);
        Height = Math.Min(Theme.S(700), screenArea.Height);
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
        var topPanel = new BufferedPanel { Dock = DockStyle.Top, Height = Theme.S(124) };
        Theme.StyleContainer(topPanel);
        _topPanel = topPanel;

        btnLaunch = new FlatButton
        {
            Text = "Launch Ashes of Erebus",
            Width = Theme.S(440),
            Height = Theme.S(66),
            Top = Theme.S(10),
            Font = Theme.HeadingFont(1.75f),
        };
        Theme.StyleButton(btnLaunch, primary: true);
        btnLaunch.Click += (s, e) => LaunchGame();

        var btnCiv4Config = new FlatButton { Text = "Open Civ4 Config", Width = ConfigButtonWidth, Height = Theme.ButtonHeight, Top = Theme.S(10) };
        Theme.StyleButton(btnCiv4Config);
        btnCiv4Config.Click += (s, e) => OpenCiv4Config();

        // Toggles the module lists + preset tools; centered on its own row beneath Launch.
        btnManage = new FlatButton { Text = "Manage Modules (Custom)", Width = Theme.S(165), Height = Theme.ButtonHeight, Top = Theme.S(10) + Theme.S(66) + Theme.S(8) };
        Theme.StyleButton(btnManage);
        btnManage.Click += (s, e) =>
        {
            var show = !_config.ModulesVisible;
            ApplyModulesVisibility(show, initial: false);
            _config.ModulesVisible = show;
            SaveConfig();
        };

        // Sized from the measured text rather than AutoSize, so its width is already correct
        // when the Resize handler below centers it (AutoSize only settles after layout).
        chkCloseOnLaunch = new CheckBox
        {
            Text = "Close on launch?",
            Top = Theme.S(10) + Theme.ButtonHeight + Theme.S(12),
            Height = Theme.BodyFont.Height + Theme.S(8),
            Font = Theme.BodyFont,
        };
        chkCloseOnLaunch.Width = FittedCheckBoxWidth(chkCloseOnLaunch);
        Theme.StyleCheckBox(chkCloseOnLaunch);
        // The CheckedChanged handler (which saves the setting) is attached in MainForm_Load,
        // after the saved value has been applied, so loading the config doesn't trigger a save.

        var btnHelp = new FlatButton { Text = "Instructions", Left = Theme.S(12), Top = Theme.S(10), Width = HelpButtonWidth, Height = Theme.ButtonHeight };
        Theme.StyleButton(btnHelp);
        btnHelp.Click += (s, e) => ShowHelp();

        // Main status readout, the mirror image of the Close on launch checkbox: same row, same
        // height, centered under the Instructions button. Filled in by UpdateStatusIndicator.
        _statusIndicator = new StatusIndicator { Top = chkCloseOnLaunch.Top, Height = chkCloseOnLaunch.Height };
        _statusIndicator.Width = _statusIndicator.MeasureWidth(StatusValues);
        _statusIndicator.SetStatus("Ready", Theme.StatusGood);
        _statusIndicator.MouseEnter += (s, args) => CheckGameRunning();

        _presetToolTip.SetToolTip(btnLaunch, "Starts Ashes of Erebus with the active modules (they are checked first).");
        _presetToolTip.SetToolTip(btnCiv4Config, "Opens your Civ4 config .ini file in your default text editor.");
        _presetToolTip.SetToolTip(btnManage, "Shows or hides the module lists and preset tools. In brackets: the saved preset your active modules currently match, or Custom.");
        _presetToolTip.SetToolTip(chkCloseOnLaunch, "Closes this launcher once the game has started.");
        _presetToolTip.SetToolTip(btnHelp, "Shows the usage guide.");

        topPanel.Controls.Add(btnHelp);
        topPanel.Controls.Add(btnLaunch);
        topPanel.Controls.Add(btnCiv4Config);
        topPanel.Controls.Add(btnManage);
        topPanel.Controls.Add(chkCloseOnLaunch);
        topPanel.Controls.Add(_statusIndicator);
        topPanel.Resize += (s, e) =>
        {
            btnLaunch.Left = (topPanel.Width - btnLaunch.Width) / 2;
            CenterManageButton();
            btnCiv4Config.Left = topPanel.Width - btnCiv4Config.Width - Theme.S(12);

            // Each readout is centered under the button above it.
            chkCloseOnLaunch.Left = btnCiv4Config.Left + (btnCiv4Config.Width - chkCloseOnLaunch.Width) / 2;
            _statusIndicator.Left = Math.Max(0, btnHelp.Left + (btnHelp.Width - _statusIndicator.Width) / 2);
        };

        _splitContainer = new BufferedSplitContainer
        {
            Dock = DockStyle.Fill,
            Orientation = Orientation.Vertical,
            IsSplitterFixed = true, // panes are always an even 50/50 split -- no draggable divider
            SplitterWidth = Theme.S(3),
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

        foreach (var g in new[] { dgvActive, dgvInactive }) WireColumnLayout(g);
        if (_config.AuthorColumnWidth > 0)
            SetAuthorWidth(Math.Max(MinAuthorWidth, _config.AuthorColumnWidth), fromUser: false);

        _splitContainer.Panel1.Controls.Add(activeGroup);
        _splitContainer.Panel2.Controls.Add(inactiveGroup);

        // Tag filter section, centered between the module lists and the preset tools: a larger
        // "Filters:" heading on its own row, the filter boxes on the row below it, and a thin
        // separator line along the bottom edge to set it apart from the preset/refresh row.
        var filterPanel = new BufferedPanel { Height = FilterPanelHeight };
        Theme.StyleContainer(filterPanel);
        _filterPanel = filterPanel;

        var lblFilters = new Label
        {
            Text = "Filters:",
            AutoSize = false,
            TextAlign = ContentAlignment.MiddleCenter,
            Font = Theme.HeadingFont(SectionHeadingScale),
        };
        lblFilters.Width = TextRenderer.MeasureText(lblFilters.Text, lblFilters.Font).Width + Theme.S(12);
        lblFilters.Height = lblFilters.Font.Height + Theme.S(4);
        Theme.StyleLabel(lblFilters);
        filterPanel.Controls.Add(lblFilters);

        _filterToolTip.SetToolTip(lblFilters,
            "Click a tag's box to cycle it: empty = no filter, white = only show modules WITH the tag, " +
            "black = grey out modules WITH the tag. Right-click a box to clear it.\n" +
            "Greyed-out modules are moved to the bottom of their list but are still active/inactive as before.");
        foreach (var (tag, label) in FilterTags)
        {
            // Text is the label shown to the user; Tag keeps the info.txt token used for matching.
            var box = new TagFilterBox { Text = label, Tag = tag, Font = Theme.BodyFont };
            box.FitToText();
            box.StateChanged += (s, e) => OnFilterChanged();
            _filterToolTip.SetToolTip(box,
                $"{label}: click to cycle (empty = no filter, white = only {label} modules, black = hide {label} modules). Right-click to clear.");
            _filterBoxes.Add(box);
            filterPanel.Controls.Add(box);
        }

        void LayoutFilterRow()
        {
            int spacing = Theme.S(24); // gap between filter sets (was 20; +20%)
            int topPad = Theme.S(4);

            lblFilters.Left = (filterPanel.Width - lblFilters.Width) / 2;
            lblFilters.Top = topPad;

            var total = _filterBoxes.Sum(c => c.Width) + spacing * (_filterBoxes.Count - 1);
            var x = Math.Max(0, (filterPanel.Width - total) / 2);
            var boxesTop = lblFilters.Bottom + Theme.S(2);
            foreach (var c in _filterBoxes)
            {
                c.Left = x;
                c.Top = boxesTop;
                x += c.Width + spacing;
            }
            filterPanel.Invalidate();
        }
        filterPanel.Resize += (s, e) => LayoutFilterRow();
        filterPanel.Paint += (s, e) =>
        {
            using var pen = new Pen(Theme.GridLine);
            var y = filterPanel.Height - 2;
            e.Graphics.DrawLine(pen, Theme.S(12), y, filterPanel.Width - Theme.S(12), y);
        };
        LayoutFilterRow();

        var bottomPanel = new BufferedPanel { Height = PresetPanelHeight };
        Theme.StyleContainer(bottomPanel);
        _bottomPanel = bottomPanel;

        // "Presets:" heading, centered, in the same style as "Filters:" -- just below the separator line.
        var lblPresets = new Label
        {
            Text = "Presets:",
            AutoSize = false,
            TextAlign = ContentAlignment.MiddleCenter,
            Font = Theme.HeadingFont(SectionHeadingScale),
        };
        lblPresets.Width = TextRenderer.MeasureText(lblPresets.Text, lblPresets.Font).Width + Theme.S(12);
        lblPresets.Height = lblPresets.Font.Height + Theme.S(4);
        lblPresets.Top = Theme.S(4);
        Theme.StyleLabel(lblPresets);

        var row1Top = PresetRowsTop;
        var row2Top = PresetRowsTop + Theme.ButtonHeight + Theme.S(8);

        // Row 1: save on the left, the Load | dropdown | Delete group centered, Refresh on the right
        var btnSave = new FlatButton { Text = SaveButtonText, Left = Theme.S(12), Top = row1Top, Width = PresetButtonWidth, Height = Theme.ButtonHeight };
        btnLoadPreset = new FlatButton { Text = "Load Preset", Top = row1Top, Width = PresetSideButtonWidth, Height = Theme.ButtonHeight };
        cmbPresets = new ComboBox { Top = row1Top + (Theme.ButtonHeight - (Theme.BodyFont.Height + Theme.S(6))) / 2, Width = PresetComboWidth, DropDownStyle = ComboBoxStyle.DropDownList };
        btnDeletePreset = new FlatButton { Text = "Delete Preset", Top = row1Top, Width = PresetSideButtonWidth, Height = Theme.ButtonHeight };
        var btnRefresh = new FlatButton { Text = "Refresh", Top = row1Top, Width = RefreshButtonWidth, Height = Theme.ButtonHeight };
        Theme.StyleButton(btnSave);
        Theme.StyleComboBox(cmbPresets);
        Theme.StyleButton(btnLoadPreset);
        Theme.StyleButton(btnDeletePreset);
        Theme.StyleButton(btnRefresh);
        // Pressing Refresh re-checks every module's hardcoded paths into other modules' folders first
        // (see CrossModulePathScanner), then re-reads the modules, e.g. after moving them in Explorer.
        btnRefresh.Click += (s, e) =>
        {
            _reportedInactiveRefs.Clear(); // a manual refresh may show the inactive-reference notice again
            EnsureCrossModulePaths(abortAction: null);
            var summary = _lastScanSummary;
            RefreshModules();
            if (summary != null) lblStatus.Text = summary + "  " + lblStatus.Text;
        };

        // Row 2: export (under Save, same width) + Futureproof (under it, left of the dropdown) +
        // import (centered under the dropdown), with the dev action right-aligned
        var btnExport = new FlatButton { Text = ExportButtonText, Left = Theme.S(12), Top = row2Top, Width = PresetButtonWidth, Height = Theme.ButtonHeight };
        var btnImport = new FlatButton { Text = "Import Preset", Top = row2Top, Width = PresetImportButtonWidth, Height = Theme.ButtonHeight };
        chkFutureproof = new CheckBox
        {
            Text = FutureproofText,
            AutoSize = false,
            Font = Theme.BodyFont,
            Left = FutureproofLeftPx, Top = row2Top + (Theme.ButtonHeight - (Theme.BodyFont.Height + Theme.S(8))) / 2, Height = Theme.BodyFont.Height + Theme.S(8), Width = FutureproofWidth,
        };
        var btnDevSchemas = new FlatButton { Text = "Dev: Update Schemas", Top = row2Top, Width = SchemasButtonWidth, Height = Theme.ButtonHeight };
        Theme.StyleButton(btnImport);
        Theme.StyleCheckBox(chkFutureproof);
        Theme.StyleButton(btnExport);
        Theme.StyleButton(btnDevSchemas);
        btnDevSchemas.Click += (s, e) => UpdateSchemas();

        _presetToolTip.SetToolTip(chkFutureproof, FutureproofTip);
        _presetToolTip.SetToolTip(btnSave, "Saves the active modules, with their Load #s, as a new preset. With Futureproof checked, versions and fingerprints are left out.");
        _presetToolTip.SetToolTip(btnRefresh, "Re-checks the file paths between modules, then re-reads the module folders. Use it after moving modules by hand.");
        _presetToolTip.SetToolTip(btnExport, "Copies a share code for your active modules and their Load #s to the clipboard, e.g. to post on Discord.");
        _presetToolTip.SetToolTip(btnImport, "Imports a preset from a share code, then offers to apply it.");
        _presetToolTip.SetToolTip(btnDevSchemas, "For module makers: updates modules' *Schema.xml files from the base mod (a preview is shown first).");

        btnSave.Click += (s, e) => SavePreset();
        btnLoadPreset.Click += (s, e) => LoadPreset();
        btnDeletePreset.Click += (s, e) => DeletePreset();
        cmbPresets.SelectedIndexChanged += (s, e) => UpdatePresetButtons();
        btnExport.Click += (s, e) => ExportPreset();
        btnImport.Click += (s, e) => ImportPreset();

        bottomPanel.Controls.AddRange(new Control[]
        {
            lblPresets, btnSave, cmbPresets, btnLoadPreset, btnDeletePreset, btnRefresh, btnImport, btnExport, chkFutureproof, btnDevSchemas
        });
        bottomPanel.Resize += (s, e) =>
        {
            lblPresets.Left = (bottomPanel.Width - lblPresets.Width) / 2;
            btnRefresh.Left = bottomPanel.Width - btnRefresh.Width - Theme.S(12);

            // Load | dropdown | Delete are centered in the row; Import is centered under the dropdown.
            var left = (bottomPanel.Width - PresetGroupWidth) / 2;
            btnLoadPreset.Left = left;
            cmbPresets.Left = btnLoadPreset.Right + Theme.S(8);
            btnDeletePreset.Left = cmbPresets.Right + Theme.S(8);
            btnImport.Left = cmbPresets.Left + (cmbPresets.Width - btnImport.Width) / 2;

            btnDevSchemas.Left = bottomPanel.Width - btnDevSchemas.Width - Theme.S(12);
            // Safety net: never let the checkbox (and its background) extend under the Import button.
            chkFutureproof.Width = Math.Max(Theme.S(60),
                Math.Min(FutureproofWidth, btnImport.Left - chkFutureproof.Left - Theme.S(8)));
        };

        // Status bar: status text fills the left, launcher version sits at the right.
        var statusPanel = new BufferedPanel { Dock = DockStyle.Bottom, Height = Theme.BodyFont.Height + Theme.S(12) };
        Theme.StyleContainer(statusPanel);
        _statusPanel = statusPanel;

        lblStatus = new Label
        {
            Dock = DockStyle.Fill,
            TextAlign = ContentAlignment.MiddleLeft,
            Padding = new Padding(Theme.S(10), 0, 0, 0),
            Text = "",
        };
        Theme.StyleLabel(lblStatus, muted: true);
        lblStatus.BackColor = Theme.Panel;

        var lblLauncherVersion = new Label
        {
            Dock = DockStyle.Right,
            AutoSize = true,
            TextAlign = ContentAlignment.MiddleRight,
            Padding = new Padding(0, 0, Theme.S(10), 0),
            Text = $"Launcher v{LauncherVersion}",
        };
        Theme.StyleLabel(lblLauncherVersion, muted: true);
        lblLauncherVersion.BackColor = Theme.Panel;

        // Fill control goes in first so the Right-docked label claims its space before it.
        statusPanel.Controls.Add(lblStatus);
        statusPanel.Controls.Add(lblLauncherVersion);

        // The filter row and the preset rows live in one bottom-docked block with fixed, explicit
        // positions (filters on top, presets underneath). Previously each was its own bottom-docked
        // panel, and WinForms decides the order of same-edge docked controls purely from their
        // z-order -- so anything that shuffled the z-order could put the filters under the presets.
        var bottomStack = new BufferedPanel { Dock = DockStyle.Bottom, Height = filterPanel.Height + bottomPanel.Height };
        Theme.StyleContainer(bottomStack);
        _bottomStack = bottomStack;
        filterPanel.SetBounds(0, 0, bottomStack.Width, filterPanel.Height);
        bottomPanel.SetBounds(0, filterPanel.Height, bottomStack.Width, bottomPanel.Height);
        bottomStack.Controls.Add(filterPanel);
        bottomStack.Controls.Add(bottomPanel);
        bottomStack.Resize += (s, e) =>
        {
            filterPanel.SetBounds(0, 0, bottomStack.ClientSize.Width, filterPanel.Height);
            bottomPanel.SetBounds(0, filterPanel.Height, bottomStack.ClientSize.Width, bottomPanel.Height);
        };

        // Dock order is z-order: the Fill control must be first (frontmost) so it is docked last,
        // and the edge panels are then docked from the last one inwards. Set explicitly.
        Controls.Add(_splitContainer);
        Controls.Add(bottomStack);
        Controls.Add(statusPanel);
        Controls.Add(topPanel);
        Controls.SetChildIndex(_splitContainer, 0);
        Controls.SetChildIndex(bottomStack, 1);
        Controls.SetChildIndex(statusPanel, 2);
        Controls.SetChildIndex(topPanel, 3);
    }

    // ------------------------------------------------- Manage Modules button ---

    private static readonly int ManageButtonMinWidth = Theme.S(165);
    private static readonly int ManageButtonMaxWidth = Theme.S(380);

    /// The preset the active modules currently match (cached; "Custom" if none). Recomputed by
    /// RecomputeCurrentPreset whenever the modules or the presets change, because the full match
    /// includes content fingerprints, which are too expensive to recompute on every redraw.
    private string _currentPresetLabel = "Custom";

    /// Finds the saved preset that matches the active modules exactly: the same set of module
    /// folders, the same Load # for every module the preset records one for, AND the same content
    /// fingerprint for every module the preset records one for (a preset saved or imported as
    /// "futureproof" has none, so for those only the module set and Load #s are compared). A module
    /// that changed since the preset was saved therefore makes the label "Custom". If several
    /// presets match, the first by name wins.
    /// The cheap checks (names, Load #s) run first and fingerprints are only computed for modules
    /// of presets that pass them, each at most once per call.
    private void RecomputeCurrentPreset()
    {
        _currentPresetLabel = FindMatchingPresetName() ?? "Custom";
    }

    /// `knownFingerprints` (folder name -> fingerprint) lets a caller that has just computed them
    /// avoid doing it twice; any missing ones are computed (and added) here.
    private string? FindMatchingPresetName(Dictionary<string, string>? knownFingerprints = null)
    {
        var active = _activeModules.ToDictionary(m => m.FolderName, m => m, StringComparer.OrdinalIgnoreCase);
        var fingerprints = knownFingerprints ?? new Dictionary<string, string>(StringComparer.OrdinalIgnoreCase);

        foreach (var preset in _config.Presets.OrderBy(p => p.Name, StringComparer.OrdinalIgnoreCase))
        {
            var names = new HashSet<string>(preset.Modules.Select(m => m.Name), StringComparer.OrdinalIgnoreCase);
            if (names.Count != active.Count) continue;

            var same = true;
            foreach (var pm in preset.Modules)
            {
                if (!active.TryGetValue(pm.Name, out var local)) { same = false; break; }
                var wanted = ModuleLayout.NormalizePass(pm.LoadPass);
                if (wanted.Length > 0 && !string.Equals(wanted, local.LoadPass, StringComparison.Ordinal)) { same = false; break; }
            }
            if (!same) continue;

            foreach (var pm in preset.Modules)
            {
                if (string.IsNullOrEmpty(pm.Fingerprint)) continue;
                var local = active[pm.Name];
                if (!fingerprints.TryGetValue(pm.Name, out var fp))
                {
                    SetStatus($"Comparing active modules with saved presets: '{local.Name}'...");
                    fingerprints[pm.Name] = fp = ModuleScanner.ComputeFingerprint(local.FullPath);
                }
                if (!string.Equals(fp, pm.Fingerprint, StringComparison.Ordinal)) { same = false; break; }
            }
            if (same) return preset.Name;
        }
        return null;
    }

    /// Sets the toggle button's text to "Manage Modules (<preset>)" / "Hide Modules (<preset>)", where
    /// <preset> is the matching saved preset or "Custom", and sizes it to fit (within a fixed
    /// maximum; a very long preset name is cut short with an ellipsis).
    private void UpdateManageButton(bool? modulesVisible = null)
    {
        if (btnManage == null) return;

        var prefix = (modulesVisible ?? _config.ModulesVisible) ? "Hide Modules" : "Manage Modules";
        var label = _currentPresetLabel;

        string Build(string l) => $"{prefix} ({l})";
        int Measure(string t) => TextRenderer.MeasureText(t, btnManage.Font, Size.Empty, TextFormatFlags.NoPadding | TextFormatFlags.SingleLine).Width
                                 + Theme.S(24); // side padding + border

        var text = Build(label);
        while (Measure(text) > ManageButtonMaxWidth && label.Length > 1)
        {
            label = label.Substring(0, label.Length - 1);
            text = Build(label.TrimEnd() + "\u2026");
        }

        btnManage.Text = text;
        btnManage.Width = Math.Max(ManageButtonMinWidth, Math.Min(ManageButtonMaxWidth, Measure(text)));
        CenterManageButton();
    }

    private void CenterManageButton()
    {
        if (_topPanel == null || btnManage == null) return;
        btnManage.Left = (_topPanel.Width - btnManage.Width) / 2;
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
            _bottomStack.Visible = true;
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
            _bottomStack.Visible = false;
            MaximizeBox = false;
            ApplyCollapsedSize();
        }

        UpdateManageButton(show);
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
            Font = Theme.BodyFont,
        };
        Theme.StyleGrid(grid);
        grid.ColumnHeadersHeight = Theme.BodyFont.Height + Theme.S(14);
        grid.RowTemplate.Height = Theme.BodyFont.Height + Theme.S(10);

        var nameCol = new DataGridViewTextBoxColumn
        {
            Name = "Name", HeaderText = "Module",
            // Sized by FitNameColumn (fills whatever the other columns leave) rather than the
            // built-in Fill mode, so that dragging the Module|Author divider can be turned into an
            // Author width change that is mirrored in both lists.
            AutoSizeMode = DataGridViewAutoSizeColumnMode.None,
            Width = Theme.S(200),
            MinimumWidth = MinNameWidth,
            Resizable = DataGridViewTriState.False, // the divider is dragged via ModuleGridView.DividerDragged
        };

        var authorCol = new DataGridViewTextBoxColumn
        {
            Name = "Author", HeaderText = "Author",
            AutoSizeMode = DataGridViewAutoSizeColumnMode.None,
            Width = DefaultAuthorWidth,
            MinimumWidth = MinAuthorWidth,
            Resizable = DataGridViewTriState.False,
        };

        // Fixed-width, non-resizable column whose width is derived from its header text (and any
        // sample content that must fit) in the grid's own font, plus a little padding -- and room
        // for the sort arrow when the column is sortable.
        DataGridViewTextBoxColumn FittedCol(string name, string header, bool sortable, bool centered = false, string sample = "")
        {
            var col = new DataGridViewTextBoxColumn
            {
                Name = name, HeaderText = header,
                AutoSizeMode = DataGridViewAutoSizeColumnMode.None,
                Resizable = DataGridViewTriState.False,
                SortMode = sortable ? DataGridViewColumnSortMode.Automatic : DataGridViewColumnSortMode.NotSortable,
            };
            col.Width = FittedWidth(grid, header, sample, sortable);
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
            Resizable = DataGridViewTriState.False,
            SortMode = DataGridViewColumnSortMode.NotSortable,
            FlatStyle = FlatStyle.Flat,
        };
        infoCol.Width = FittedWidth(grid, "Info", "i", sortable: false);

        // Module | Author | M. Ver | AoE Ver | Load # | Info
        // M. Ver is deliberately not sortable; AoE Ver and Load # are (see OnGridSortCompare).
        grid.Columns.AddRange(
            nameCol,
            authorCol,
            FittedCol("Version", "M. Ver", sortable: false),
            FittedCol("AoERev", "AoE Ver", sortable: true),
            FittedCol("LoadPass", "Load #", sortable: true, centered: true, sample: "0"),
            infoCol);

        // Mouseover tooltips for the column headers (drawn by ModuleGridView).
        void Tip(string column, string text) => grid.Columns[column]!.HeaderCell.ToolTipText = text;
        Tip("Name", "The module's declared name (the [name] entry in its info.txt). It can differ slightly from the name of the folder that contains it.");
        Tip("Author", "Who made the module. Thank your modders!");
        Tip("Version", "Module version: the version of this module itself, as declared by its author.");
        Tip("AoERev", "AoE version: the version of Ashes of Erebus this module was last updated for. Click to sort.");
        Tip("LoadPass", "Load #: which load folder (0-4) the module is in. The game loads 0 first, then 1, 2, 3 and 4, and alphabetically by folder name within each. Right-click a module to change it. Click to sort.");
        Tip("Info", "Click the \"i\" button on a row to see the module's full description, author, versions, load #, and its dependency and compatibility lists.");
        return grid;
    }

    // ------------------------------------------------------- Grid columns ---

    private static readonly int DefaultAuthorWidth = Theme.S(60);
    private static readonly int MinAuthorWidth = Theme.S(40);
    private static readonly int MinNameWidth = Theme.S(100);

    /// True while the code itself is changing column widths, so those changes aren't mistaken
    /// for the user dragging a divider.
    private bool _columnLayoutBusy;

    /// The Author width changed by user dragging and hasn't been written to the config file yet.
    private bool _authorWidthDirty;

    /// Width of a CheckBox sized to its content: the box glyph plus the text plus a few pixels,
    /// with no spare room, so that centering the control also centers what you actually see.
    private static int FittedCheckBoxWidth(CheckBox box)
    {
        int glyph;
        try
        {
            using var g = Graphics.FromHwnd(IntPtr.Zero);
            glyph = CheckBoxRenderer.GetGlyphSize(g, System.Windows.Forms.VisualStyles.CheckBoxState.UncheckedNormal).Width;
        }
        catch
        {
            glyph = 16;
        }

        var text = TextRenderer.MeasureText(box.Text, box.Font, Size.Empty,
            TextFormatFlags.NoPadding | TextFormatFlags.SingleLine).Width;
        return glyph + text + Theme.S(6);
    }

    /// Width that exactly fits a header (and optional sample cell text) in the grid's fonts, with
    /// small padding, plus room for the sort arrow if the column is sortable.
    private static int FittedWidth(DataGridView grid, string header, string sample, bool sortable)
    {
        const TextFormatFlags flags = TextFormatFlags.NoPadding | TextFormatFlags.SingleLine;
        var headerFont = grid.ColumnHeadersDefaultCellStyle.Font ?? grid.Font;
        var cellFont = grid.DefaultCellStyle.Font ?? grid.Font;

        var width = TextRenderer.MeasureText(header, headerFont, Size.Empty, flags).Width;
        if (sortable) width += Theme.S(6); // the sort glyph is drawn at the right of the header text
        if (sample.Length > 0)
            width = Math.Max(width, TextRenderer.MeasureText(sample, cellFont, Size.Empty, flags).Width);
        return width + Theme.S(4); // cell padding and borders
    }

    /// Hooks a grid up to the column behaviour: keeping the Module column filling the remaining
    /// width, turning divider drags into a synchronized Author width, and custom sort orders.
    private void WireColumnLayout(ModuleGridView grid)
    {
        grid.SizeChanged += (s, e) => FitNameColumn(grid);
        grid.RowsAdded += (s, e) => FitNameColumn(grid);
        grid.RowsRemoved += (s, e) => FitNameColumn(grid);
        var vScroll = grid.Controls.OfType<VScrollBar>().FirstOrDefault();
        if (vScroll != null) vScroll.VisibleChanged += (s, e) => FitNameColumn(grid);

        grid.DividerDragged += (s, desiredNameWidth) => OnDividerDragged(grid, desiredNameWidth);
        grid.DividerDragEnded += (s, e) =>
        {
            if (!_authorWidthDirty) return;
            _authorWidthDirty = false;
            SaveConfig();
        };
        grid.SortCompare += OnGridSortCompare;
    }

    private static int AvailableWidth(DataGridView grid)
    {
        var vScroll = grid.Controls.OfType<VScrollBar>().FirstOrDefault();
        return grid.ClientSize.Width - (vScroll != null && vScroll.Visible ? vScroll.Width : 0);
    }

    /// Total width of every column except Module and Author.
    private static int OtherFixedWidth(DataGridView grid) =>
        grid.Columns.Cast<DataGridViewColumn>()
            .Where(c => c.Visible && c.Name != "Name" && c.Name != "Author")
            .Sum(c => c.Width);

    /// Makes the Module column take whatever width the other columns leave over.
    private void FitNameColumn(DataGridView grid)
    {
        if (_columnLayoutBusy || grid.Columns.Count == 0) return;
        var name = grid.Columns["Name"];
        if (name == null) return;

        var target = Math.Max(MinNameWidth, AvailableWidth(grid) - OtherFixedWidth(grid) - grid.Columns["Author"]!.Width);
        if (name.Width == target) return;

        _columnLayoutBusy = true;
        try { name.Width = target; }
        finally { _columnLayoutBusy = false; }
    }

    /// The user is dragging the Module|Author divider and wants the Module column to be
    /// `desiredNameWidth` wide: that becomes a new Author width (everything right of the divider is
    /// fixed width), applied live to both lists, with the Module column re-filling the rest.
    private void OnDividerDragged(DataGridView grid, int desiredNameWidth)
    {
        var other = OtherFixedWidth(grid);
        var available = AvailableWidth(grid);
        var wanted = available - other - desiredNameWidth;
        var max = Math.Max(MinAuthorWidth, available - other - MinNameWidth);
        SetAuthorWidth(Math.Max(MinAuthorWidth, Math.Min(wanted, max)), fromUser: true);
    }

    /// Sets the Author width of both lists and re-fits their Module columns.
    private void SetAuthorWidth(int width, bool fromUser)
    {
        foreach (var g in new[] { dgvActive, dgvInactive })
        {
            var author = g.Columns["Author"];
            if (author == null) continue;
            if (author.Width != width)
            {
                _columnLayoutBusy = true;
                try { author.Width = width; }
                finally { _columnLayoutBusy = false; }
            }
            FitNameColumn(g);
        }

        if (fromUser && _config.AuthorColumnWidth != width)
        {
            _config.AuthorColumnWidth = width;
            _authorWidthDirty = true;
        }
    }

    /// Sort order for the two sortable non-text-like columns: AoE Ver numerically (blank first),
    /// Load # in load order (0, 1, 2, 3, 4). Ties fall back to the module name. Modules
    /// greyed out by the tag filters stay after the others in either direction.
    private void OnGridSortCompare(object? sender, DataGridViewSortCompareEventArgs e)
    {
        if (sender is not DataGridView grid) return;
        if (grid.Rows[e.RowIndex1].Tag is not ModuleInfo a || grid.Rows[e.RowIndex2].Tag is not ModuleInfo b) return;

        int result = (IsFilteredOut(a) ? 1 : 0) - (IsFilteredOut(b) ? 1 : 0);
        if (result != 0)
        {
            // The grid flips the result for a descending sort, so pre-flip it to keep these at the bottom.
            e.SortResult = grid.SortOrder == SortOrder.Descending ? -result : result;
            e.Handled = true;
            return;
        }

        switch (e.Column.Name)
        {
            case "AoERev":
                result = int.TryParse(a.AoeRev, out var ra) && int.TryParse(b.AoeRev, out var rb)
                    ? ra.CompareTo(rb)
                    : string.Compare(a.AoeRev, b.AoeRev, StringComparison.OrdinalIgnoreCase);
                break;
            case "LoadPass":
                result = ModuleLayout.PassIndex(a.LoadPass).CompareTo(ModuleLayout.PassIndex(b.LoadPass));
                break;
            default:
                return; // other columns use the grid's default text comparison
        }

        if (result == 0)
            result = string.Compare(a.Name, b.Name, StringComparison.OrdinalIgnoreCase);
        e.SortResult = result;
        e.Handled = true;
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
        RefreshPresetCombo(updateManageButton: false); // RefreshModules already matched the presets
    }

    /// Returns true if the app should proceed, false if the user chose to quit.
    private bool ResolvePlacementIssues(PlacementResult initial)
    {
        var placement = initial;
        while (true)
        {
            var msg = new StringBuilder();
            msg.AppendLine(BuildPlacementIssuesText(placement));
            msg.AppendLine();
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
                        _installIssueText = null;
                        return true;
                    }
                    continue;

                case PlacementChoice.ContinueAnyway:
                    _btsExePath = placement.BtsExePath; // may still be null, that's fine -- Launch will just report it clearly
                    _installIssueText = BuildPlacementIssuesText(placement); // keeps the status indicator on "Install Error"
                    return true;

                case PlacementChoice.Quit:
                default:
                    return false;
            }
        }
    }

    /// The problem list shown by the startup setup-check popup (and, identically, by the Install
    /// Error status tooltip).
    private static string BuildPlacementIssuesText(PlacementResult placement)
    {
        var text = new StringBuilder();
        text.AppendLine("The launcher found some problems with where this folder is placed:");
        text.AppendLine();
        foreach (var err in placement.Errors)
        {
            text.AppendLine(err);
            text.AppendLine();
        }
        return text.ToString().TrimEnd();
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
            MessageBox.Show(this, GameNotFoundText, "Cannot Launch", MessageBoxButtons.OK, MessageBoxIcon.Error);
            return;
        }

        if (!ConfirmGameNotRunning("Game Already Running",
                "Launching again will start a second copy of the game, which can cause crashes, " +
                "save problems or conflicts between the two.",
                "launching the game"))
        {
            lblStatus.Text = "Launch aborted.";
            return;
        }

        if (!VerifyActiveModules("launching the game"))
        {
            lblStatus.Text = "Launch aborted.";
            return;
        }

        // Last step before starting: make sure modules' paths into other modules' folders are current.
        if (!EnsureCrossModulePaths("launching the game"))
        {
            lblStatus.Text = "Launch aborted.";
            return;
        }

        try
        {
            var modFolderName = Path.GetFileName(_modPath);
            GameLauncher.Launch(_btsExePath, modFolderName);
            lblStatus.Text = "Launching Civilization IV...";
            _gameRunning = true;
            _lastGameCheckUtc = DateTime.UtcNow;
            UpdateStatusIndicator();

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
    /// Load order problems on the active modules can be fixed on the spot with Autosort.
    private bool VerifyActiveModules(string action)
    {
        var (set, installed) = ScanActiveSet();
        return VerifyModuleSet(action, set, installed, "active", reload: ScanActiveSet);
    }

    /// A fresh scan: the active modules as load entries, plus everything installed.
    private (List<LoadEntry> Set, List<ModuleInfo> Installed) ScanActiveSet()
    {
        var installed = ModuleScanner.ScanAll(_modPath);
        var set = installed.Where(m => m.IsActive).Select(m => new LoadEntry(m, m.LoadPass)).ToList();
        return (set, installed);
    }

    // The three problem texts below are shared by the popups and by the status indicator's
    // tooltip, so the two always say the same thing. None of them includes the closing question.

    private static string BuildIncompatibleText(List<string> issues, string setDescription)
    {
        var text = new StringBuilder();
        text.AppendLine($"These modules are marked as incompatible with each other, but both are {setDescription}:");
        text.AppendLine();
        foreach (var issue in issues) text.AppendLine($"   - {issue}");
        return text.ToString().TrimEnd();
    }

    private static string BuildMissingDependencyText(List<string> issues)
    {
        var text = new StringBuilder();
        text.AppendLine("Some modules require other modules that aren't loaded. A required (hard) dependency must be " +
                        "present and load before the module that requires it.");
        text.AppendLine();
        foreach (var issue in issues)
        {
            text.AppendLine(issue);
            text.AppendLine();
        }
        return text.ToString().TrimEnd();
    }

    private static string BuildOrderText(SetAnalysis analysis)
    {
        var text = new StringBuilder();
        text.AppendLine("Some modules load before a module they depend on. Dependencies must load earlier: " +
                        "Load 0 occurs first, then 1, 2, 3, 4, and alphabetically by folder name within a Load #.");

        if (analysis.HardOrderIssues.Count > 0)
        {
            text.AppendLine();
            text.AppendLine("Required (hard) dependencies that load too late:");
            text.AppendLine();
            foreach (var issue in analysis.HardOrderIssues)
            {
                text.AppendLine(issue);
                text.AppendLine();
            }
        }

        if (analysis.SoftOrderIssues.Count > 0)
        {
            text.AppendLine();
            text.AppendLine("Optional (soft) dependencies that are loaded, but not before the module that lists them. " +
                            "Soft dependencies don't have to be present, but when they are they should load earlier:");
            text.AppendLine();
            foreach (var issue in analysis.SoftOrderIssues)
            {
                text.AppendLine(issue);
                text.AppendLine();
            }
        }

        return text.ToString().TrimEnd();
    }

    private static string BuildModuleIssueText(SetAnalysis analysis, string setDescription)
    {
        var parts = new List<string>();
        if (analysis.Incompatible.Count > 0) parts.Add(BuildIncompatibleText(analysis.Incompatible, setDescription));
        if (analysis.MissingDependencies.Count > 0) parts.Add(BuildMissingDependencyText(analysis.MissingDependencies));
        return string.Join("\n\n", parts);
    }

    /// Runs the incompatibility check, then the missing-dependency check (each with its own
    /// abort/continue popup), then the load order check (hard and soft dependencies together,
    /// one popup). Returns false as soon as the user aborts.
    /// `setDescription` completes "...is not ___" / "...both ___" in the messages.
    /// When `reload` is given (the set is the live active modules), the load order popup also
    /// offers Autosort; after a successful autosort `reload` supplies a fresh scan and the order
    /// is checked again.
    private bool VerifyModuleSet(string action, List<LoadEntry> set, List<ModuleInfo> installed, string setDescription,
        Func<(List<LoadEntry> Set, List<ModuleInfo> Installed)>? reload = null)
    {
        var analysis = ModuleChecker.Analyze(set, installed, setDescription);

        if (analysis.Incompatible.Count > 0)
        {
            var text = BuildIncompatibleText(analysis.Incompatible, setDescription) +
                       $"\n\nContinue anyway, or abort {action}?";

            if (!ShowConfirmMessage("Incompatible Modules", text, "Continue", "Abort", cancelIsDefault: true))
                return false;
        }

        if (analysis.MissingDependencies.Count > 0)
        {
            var text = BuildMissingDependencyText(analysis.MissingDependencies) +
                       $"\n\nContinue anyway, or abort {action}?";

            if (!ShowConfirmMessage("Module Dependencies", text, "Continue", "Abort", cancelIsDefault: true))
                return false;
        }

        while (analysis.HasOrderIssue)
        {
            if (reload == null)
            {
                var plain = BuildOrderText(analysis) + $"\n\nContinue anyway, or abort {action}?";
                if (!ShowConfirmMessage("Module Load Order", plain, "Continue", "Abort", cancelIsDefault: true))
                    return false;
                break;
            }

            var text = BuildOrderText(analysis) +
                       "\n\nAutosort can try to fix this by changing the Load # of some modules (you'll be shown " +
                       $"the changes and asked to confirm first). Or continue anyway, or abort {action}.";

            switch (ShowChoiceMessage("Module Load Order", text, new[] { "Autosort", "Continue", "Abort" }, defaultIndex: 2))
            {
                case 0:
                    // Applied: re-scan and re-check. Cancelled or no solution: show this popup again.
                    if (RunAutosort())
                    {
                        var fresh = reload();
                        analysis = ModuleChecker.Analyze(fresh.Set, fresh.Installed, setDescription);
                    }
                    continue;

                case 1:
                    return true;

                default:
                    return false;
            }
        }

        return true;
    }

    // ------------------------------------------------------ Status indicator ---

    /// Re-evaluates the main status readout from the startup placement check and the active modules
    /// as last scanned. Priority: Install Error, Module Issue, Bad Order, then Ready. The tooltip
    /// repeats the text of the matching popup.
    private void UpdateStatusIndicator()
    {
        string value, tip;
        Color color;

        if (_installIssueText != null || _btsExePath == null || !File.Exists(_btsExePath))
        {
            value = "Install Error";
            color = Theme.StatusError;
            tip = _installIssueText ?? GameNotFoundText;
        }
        else
        {
            var installed = _activeModules.Concat(_inactiveModules).ToList();
            var set = _activeModules.Select(m => new LoadEntry(m, m.LoadPass)).ToList();
            var analysis = ModuleChecker.Analyze(set, installed, "active");

            if (analysis.HasModuleIssue)
            {
                value = "Module Issue";
                color = Theme.StatusError;
                tip = BuildModuleIssueText(analysis, "active");
            }
            else if (analysis.HasOrderIssue)
            {
                value = "Bad Order";
                color = Theme.StatusWarning;
                tip = BuildOrderText(analysis) +
                      "\n\nRight-click a module and choose \"Autosort active modules\" to try an automatic fix.";
            }
            else if (_gameRunning)
            {
                value = "Launched";
                color = Theme.Accent;
                tip = "Civ4BeyondSword.exe is running. Module changes made now only take effect the next time the game is started.";
            }
            else
            {
                value = "Ready";
                color = Theme.StatusGood;
                tip = "The game was found, and the active modules have no incompatibilities, missing dependencies or load order problems.";
            }
        }

        _statusIndicator.SetStatus(value, color);
        _statusToolTip.SetToolTip(_statusIndicator, LimitTipLines(tip));
    }

    /// Looks for the running game (rate-limited to once a second unless forced) and returns true if
    /// the answer changed. Does not touch the UI.
    private bool RefreshGameRunning(bool force = false)
    {
        var now = DateTime.UtcNow;
        if (!force && now - _lastGameCheckUtc < GameCheckThrottle) return false;
        _lastGameCheckUtc = now;

        var running = GameLauncher.IsRunning(_btsExePath);
        if (running == _gameRunning) return false;
        _gameRunning = running;
        return true;
    }

    /// Fresh (unthrottled) check right before something that shouldn't happen under a running game.
    /// If the game is running, asks Continue/Abort; returns true if the action should go ahead.
    private bool ConfirmGameNotRunning(string title, string explanation, string abortAction)
    {
        if (RefreshGameRunning(force: true))
            UpdateStatusIndicator();
        if (!_gameRunning) return true;

        var text = "Civ4BeyondSword.exe appears to be running.\n\n" + explanation +
                   $"\n\nContinue anyway, or abort {abortAction}?";
        return ShowConfirmMessage(title, text, "Continue", "Abort", cancelIsDefault: true);
    }

    /// Checks for the running game and updates the status readout if that changed.
    private void CheckGameRunning()
    {
        if (_statusIndicator != null && RefreshGameRunning())
            UpdateStatusIndicator();
    }

    protected override void OnActivated(EventArgs e)
    {
        base.OnActivated(e);
        CheckGameRunning(); // e.g. coming back to the launcher after playing
    }

    private static string LimitTipLines(string text)
    {
        var lines = text.Replace("\r\n", "\n").Split('\n');
        if (lines.Length <= MaxStatusTipLines) return text;
        return string.Join("\n", lines.Take(MaxStatusTipLines)) +
               $"\n... and {lines.Length - MaxStatusTipLines} more lines (the full list is shown when you launch or save a preset).";
    }

    // ------------------------------------------------------------ Autosort ---

    /// "Name" or "Name (folder 'Folder')", for the autosort preview.
    private static string DescribeModule(ModuleInfo m) =>
        string.Equals(m.Name, m.FolderName, StringComparison.Ordinal) ? $"'{m.Name}'" : $"'{m.Name}' (folder '{m.FolderName}')";

    /// The "Autosort active modules" action: works out, from a fresh scan, which active modules
    /// should change Load # so every dependency loads before its dependents, shows what it would do,
    /// and only moves anything after the user applies. Returns true if changes were applied.
    /// Failing to find a solution is a normal outcome and just explains itself.
    private bool RunAutosort()
    {
        AutosortPlan plan;
        Cursor = Cursors.WaitCursor;
        try
        {
            var (set, _) = ScanActiveSet();
            plan = AutosortPlanner.Plan(set);
        }
        finally
        {
            Cursor = Cursors.Default;
        }

        if (!plan.Success)
        {
            ShowScrollableMessage("Autosort - No Solution Found",
                "Autosort couldn't find a solution, so nothing was changed.\n\n" +
                plan.FailureReason + "\n\n" +
                "This will need fixing by hand: right-click a module and choose \"Set Load # to...\", or deactivate " +
                "one of the modules involved. Autosort is only meant for simple fixes.");
            return false;
        }

        if (plan.Moves.Count == 0)
        {
            ShowScrollableMessage("Autosort",
                "Every active module's dependencies already load before it, there's nothing to change! :)");
            return false;
        }

        var preview = new StringBuilder();
        preview.AppendLine($"Autosort will change the Load # of {plan.Moves.Count} active module(s), so that every module's " +
                           "dependencies (required and optional) load before it.");
        preview.AppendLine();
        preview.AppendLine("Only modules that need to move are changed, and only to a different Load #: nothing is " +
                           "activated or deactivated, and inactive modules aren't touched. The following changes will be made:");
        preview.AppendLine();
        foreach (var move in plan.Moves)
        {
            var reason = move.Reason.Length > 0 ? $"  ({move.Reason})" : "";
            preview.AppendLine($"   - {DescribeModule(move.Module)}: {ModuleLayout.PassLabel(move.FromPass)} -> {ModuleLayout.PassLabel(move.ToPass)}{reason}");
        }

        if (!ShowConfirmMessage("Autosort - Confirm", preview.ToString(), "Apply", "Cancel"))
            return false;

        if (!PerformMoves(plan.Moves
                .Select(m => new MoveRequest { Source = m.Module.FullPath, ToActive = true, Pass = m.ToPass })
                .ToList()))
            return false;
        lblStatus.Text = $"Autosort changed the Load # of {plan.Moves.Count} module(s).";
        return true;
    }

    // ------------------------------------------------------------ Modules ---

    private void RefreshModules(bool firstLaunch = false)
    {
        Cursor = Cursors.WaitCursor;
        SetStatus("Scanning modules...");
        UpdateLaunchButtonText();

        var all = ModuleScanner.ScanAll(_modPath);
        _activeModules = all.Where(m => m.IsActive)
            .OrderBy(m => m.Name, StringComparer.OrdinalIgnoreCase).ThenBy(m => m.FolderName, StringComparer.OrdinalIgnoreCase).ToList();
        _inactiveModules = all.Where(m => !m.IsActive)
            .OrderBy(m => m.Name, StringComparer.OrdinalIgnoreCase).ThenBy(m => m.FolderName, StringComparer.OrdinalIgnoreCase).ToList();

        RepopulateGrids(keepScroll: true);
        RecomputeCurrentPreset();
        UpdateManageButton();

        // Runs once per refresh, which is once per batch of moves, never per module moved.
        RefreshGameRunning(force: true);
        UpdateStatusIndicator();

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
            var has = m.Tags.Contains(box.Tag as string ?? box.Text);
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
                m.Author, m.Version, m.AoeRev, ModuleLayout.PassDisplayName(m.LoadPass),
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

        // Rows.Clear() keeps the sort arrow but the new rows are in name order: re-apply the sort.
        if (grid.SortedColumn != null && grid.Rows.Count > 1)
            grid.Sort(grid.SortedColumn, grid.SortOrder == SortOrder.Descending
                ? System.ComponentModel.ListSortDirection.Descending
                : System.ComponentModel.ListSortDirection.Ascending);

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
        if (!string.IsNullOrWhiteSpace(m.AoeRev)) text.AppendLine($"AoE Ver: {m.AoeRev}");
        text.AppendLine($"Load #: {ModuleLayout.PassDisplayName(m.LoadPass)}");
        if (!string.Equals(m.Name, m.FolderName, StringComparison.Ordinal)) text.AppendLine($"Folder: {m.FolderName}");
        if (!string.IsNullOrWhiteSpace(m.Author)) text.AppendLine($"Author: {m.Author}");
        if (m.Compatible.Count > 0) text.AppendLine($"Compatible with: {string.Join(", ", m.Compatible)}");
        if (m.Dependencies.Count > 0) text.AppendLine($"Requires: {string.Join(", ", m.Dependencies)}");
        if (m.SoftDependencies.Count > 0) text.AppendLine($"Supports (should load after): {string.Join(", ", m.SoftDependencies)}");
        if (m.Incompatible.Count > 0) text.AppendLine($"Incompatible with: {string.Join(", ", m.Incompatible)}");
        text.AppendLine();
        text.AppendLine(!string.IsNullOrWhiteSpace(m.Desc)
            ? m.Desc
            : (!string.IsNullOrWhiteSpace(m.ShortDesc) ? m.ShortDesc : "(no description provided)"));

        ShowScrollableMessage(m.Name, text.ToString(), large: true); // module descriptions can run to thousands of characters
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
- Modules are optional addons that can be activated or disabled by this manager, visibility toggled by the Manage Modules button
- Active modules are shown on the left panel, and inactive modules on the right panel of the manager
- The Open Civ4 Config button opens your Civ4 config .ini file in your default text editor, which contains useful parameters such as showing or hiding python exceptions
- The Status readout under the Instructions button shows Ready (green), Install Error or Module Issue (red), or Bad Order (yellow); hover over it for details of what is wrong

    USING MODULES
- Changing the status of a module simply makes this launcher move the game files for you; it can be done manually
- You can either doubleclick a module to move which side it is on, or click and drag it (or a selection of multiple) across
- Shift clicking a module with one already selected will select it and all modules between the two
- Control-clicking a module will toggle the selection of that specific module without changing selection of any others
- The Refresh button will update the shown module list if you manually move files with the launcher open
- The Filters section greys out modules by tag (from each module's [tags] entry in info.txt): click a tag's box to cycle it between empty (no filter), white (only show modules WITH that tag) and black (grey out modules WITH that tag); right-click clears it
- Greyed-out modules move to the bottom of their list but are NOT removed: they stay active or inactive exactly as before, so check your filters before launching
- Right-click a module and choose ""Set Load # to..."" to move it between the Load # folders 0-4; the Load # column shows where each module currently is
- The game loads Load # 0 first, then 1, 2, 3 and 4; within each Load # modules load alphabetically by their folder name
- Moving a module between active and inactive keeps its Load #
- Before launching, saving a preset or exporting a preset, the launcher checks that no active modules are listed as incompatible with each other, and that every module's hard dependencies are active and load before it, and that any soft dependencies that are active also load before it; you can abort or continue if a problem is found
- Right-click > ""Autosort active modules"" (also offered when a load order problem is found) tries to fix load order by changing the Load # of as few active modules as it can; it shows you the changes first, and you can cancel. It is for simple fixes only: if it can't find a solution (for example, modules that depend on each other in a loop), it says so and you'll need to fix the order yourself

    PRESETS
- Pressing the ""Save Active Modules As New Preset"" button will give you the option to save the current selection as a preset (names are limited to 24 characters)
- Pressing the Load button will cause the currently selected preset in the dropdown box to be loaded
- Presets remember each module's Load #, and loading one puts modules back in those Load #s
- The Load and Delete buttons are named after the selected preset (and greyed out when there are none); hover over any button for a short description. Delete will prompt you whether to delete that preset (it will NOT delete your modules!)
- Saving, loading, exporting or importing a preset, launching, and pressing Refresh all first re-check file paths between modules, so that modules reference each other at the right Load #; moving modules between lists or Load #s does not
- If an active module refers to files in a module that is inactive, you are told once (it usually means a missing dependency)

    EXPORTING AND IMPORTING
- Presets can be exported or imported, which is VERY USEFUL when you are reporting bugs on discord
- The Import Preset button will prompt you to paste a preset code, then to name it (or press Don't save to use it without keeping it in your presets), and then offers to apply it
- Export Active Modules As Preset copies a code for your CURRENT active modules and their Load #s to your clipboard, to send to others (it first re-checks module file paths, so the code matches the files on disk). If those modules match one of your saved presets, the preset's name is shown at the start of the code
- Importing a code lets you apply it: modules are moved to the Load #s in the code (and any others deactivated), then each module is compared with the sender's copy and you are told about any that differ or are missing
- If the Futureproof box is checked, the copied code will not be checked upon import for matching module versions, only their presence (Load #s are still included); the same applies to presets you Save while it is checked

    UPDATING SCHEMAS (For module makers)
- This button will attempt to *update*, not add, schema files for all modules. The modules will need to be formatted correctly! Nonmatching schema paths will be flagged.";

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
    /// 'large' is used for the module info ("i") popup: it is sized to its text in both directions --
    /// as wide as the longest line needs (between a minimum and ~85% of the screen's working area,
    /// capped at a maximum width), then as tall as the wrapped text needs (up to ~85% of the working
    /// area, beyond which it scrolls) -- and is centered over the launcher window. The window stays resizable.
    private void ShowScrollableMessage(string title, string text, bool large = false)
    {
        var area = Screen.FromControl(this).WorkingArea;
        int width, height;
        if (large)
        {
            width = height = 0; // worked out from the text below
        }
        else
        {
            width = Math.Min(Theme.S(800), (int)(area.Width * 0.85));
            height = Math.Min(Theme.S(620), (int)(area.Height * 0.85));
        }

        using var form = new Form
        {
            Text = title,
            StartPosition = large ? FormStartPosition.Manual : FormStartPosition.CenterParent,
        };
        Theme.StyleForm(form);
        form.MinimumSize = large ? new Size(Theme.S(400), Theme.S(160)) : new Size(Theme.S(400), Theme.S(300));

        if (large)
        {
            var padding = Theme.S(12);
            var buttonHeight = Theme.ButtonHeight + Theme.S(4);
            var normalized = NormalizeNewlines(text);
            var scrollBar = SystemInformation.VerticalScrollBarWidth;
            var minWidth = Theme.S(400);
            var maxWidth = Math.Min(Theme.S(1000), (int)(area.Width * 0.85));
            var maxClientHeight = (int)(area.Height * 0.85);

            // Width: the longest single line at its natural (unwrapped) width, plus padding, the
            // scroll bar and a little slack, kept between the minimum and maximum.
            var longestLine = 0;
            foreach (var line in normalized.Split(new[] { Environment.NewLine }, StringSplitOptions.None))
            {
                if (line.Length == 0) continue;
                longestLine = Math.Max(longestLine, TextRenderer.MeasureText(line, Theme.BodyFont, Size.Empty,
                    TextFormatFlags.NoPadding | TextFormatFlags.SingleLine).Width);
            }
            width = Math.Max(minWidth, Math.Min(maxWidth, longestLine + padding * 2 + scrollBar + Theme.S(12)));

            // Height: the text wrapped the way the text box will wrap it (inside the padding, minus the
            // vertical scroll bar a multiline TextBox with ScrollBars.Vertical always reserves).
            var wrapWidth = Math.Max(Theme.S(100), width - padding * 2 - scrollBar - Theme.S(6));
            var measured = TextRenderer.MeasureText(normalized, Theme.BodyFont, new Size(wrapWidth, 0),
                TextFormatFlags.WordBreak | TextFormatFlags.TextBoxControl | TextFormatFlags.NoPadding);

            // One spare line so a wrapping estimate that is slightly off never hides the last line.
            var wanted = measured.Height + Theme.BodyFont.Height + padding * 2 + buttonHeight;
            height = Math.Max(Theme.S(140), Math.Min(maxClientHeight, wanted));
        }
        form.ClientSize = new Size(width, height);

        if (large)
        {
            // Centered over the launcher window, kept on the screen.
            var left = Left + (Width - form.Width) / 2;
            var top = Top + (Height - form.Height) / 2;
            left = Math.Max(area.Left, Math.Min(left, area.Right - form.Width));
            top = Math.Max(area.Top, Math.Min(top, area.Bottom - form.Height));
            form.Location = new Point(left, top);
        }

        var box = new ReadOnlySelectableTextBox
        {
            Dock = DockStyle.Fill,
            ScrollBars = ScrollBars.Vertical,
            Text = NormalizeNewlines(text),
            BorderStyle = BorderStyle.None,
        };
        box.BackColor = Theme.Panel;
        box.ForeColor = Theme.Text;

        // Padding around the text, so it doesn't sit flush against the window edges.
        var textHost = new Panel { Dock = DockStyle.Fill, Padding = new Padding(Theme.S(12)) };
        Theme.StyleContainer(textHost);
        textHost.Controls.Add(box);

        var okBtn = new FlatButton { Text = "OK", Dock = DockStyle.Bottom, Height = Theme.ButtonHeight + Theme.S(4), DialogResult = DialogResult.OK };
        Theme.StyleButton(okBtn, primary: true);

        form.Controls.Add(textHost);
        form.Controls.Add(okBtn);
        form.AcceptButton = okBtn;
        form.ShowDialog(this);
    }

    /// Same as ShowScrollableMessage but with Apply/Cancel, returning true if the user confirmed.
    private bool ShowConfirmMessage(string title, string text, string confirmText = "Apply", string cancelText = "Cancel",
        bool cancelIsDefault = false) =>
        ShowChoiceMessage(title, text, new[] { confirmText, cancelText }, cancelIsDefault ? 1 : 0) == 0;

    /// Scrollable read-only message with a row of right-aligned buttons. Returns the index of the
    /// button pressed, or -1 if the window was closed another way. The last button is the
    /// cancel/abort one (Escape presses it); `defaultIndex` is the one Enter presses.
    private int ShowChoiceMessage(string title, string text, string[] buttonTexts, int defaultIndex)
    {
        var area = Screen.FromControl(this).WorkingArea;
        using var form = new Form
        {
            Text = title,
            StartPosition = FormStartPosition.CenterParent,
        };
        Theme.StyleForm(form);
        form.ClientSize = new Size(
            Math.Min(Theme.S(820), (int)(area.Width * 0.85)),
            Math.Min(Theme.S(640), (int)(area.Height * 0.85)));
        form.MinimumSize = new Size(Theme.S(400), Theme.S(300));

        var box = new ReadOnlySelectableTextBox
        {
            Dock = DockStyle.Fill,
            ScrollBars = ScrollBars.Vertical,
            Text = NormalizeNewlines(text),
            BorderStyle = BorderStyle.None,
        };
        box.BackColor = Theme.Panel;
        box.ForeColor = Theme.Text;

        var textHost = new Panel { Dock = DockStyle.Fill, Padding = new Padding(Theme.S(12)) };
        Theme.StyleContainer(textHost);
        textHost.Controls.Add(box);

        var buttonPanel = new Panel { Dock = DockStyle.Bottom, Height = Theme.ButtonHeight + Theme.S(14) };
        Theme.StyleContainer(buttonPanel);

        int chosen = -1;
        var buttons = new List<FlatButton>();
        for (int i = 0; i < buttonTexts.Length; i++)
        {
            var index = i;
            var textWidth = TextRenderer.MeasureText(buttonTexts[i], Theme.BodyFont).Width;
            var btn = new FlatButton
            {
                Text = buttonTexts[i],
                Width = Math.Max(Theme.S(125), textWidth + Theme.S(24)),
                Height = Theme.ButtonHeight,
                Top = Theme.S(7),
            };
            Theme.StyleButton(btn, primary: i == defaultIndex);
            btn.Click += (s, e) =>
            {
                chosen = index;
                form.DialogResult = index == buttonTexts.Length - 1 ? DialogResult.Cancel : DialogResult.OK;
            };
            buttons.Add(btn);
            buttonPanel.Controls.Add(btn);
        }

        buttonPanel.Resize += (s, e) =>
        {
            var x = buttonPanel.Width - Theme.S(12);
            for (int i = buttons.Count - 1; i >= 0; i--)
            {
                x -= buttons[i].Width;
                buttons[i].Left = x;
                x -= Theme.S(8);
            }
        };

        form.Controls.Add(textHost);
        form.Controls.Add(buttonPanel);
        form.AcceptButton = buttons[Math.Max(0, Math.Min(defaultIndex, buttons.Count - 1))];
        form.CancelButton = buttons[buttons.Count - 1];

        form.ShowDialog(this);
        return chosen;
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
            ShowScrollableMessage("Update Schemas", "Every schema file already matches the base mod. Nothing to update!");
            return;
        }

        var preview = new StringBuilder();
        var modulesWithUpdates = plan.ModuleReports.Count(r => r.UpdatedCount > 0);
        preview.AppendLine($"This will update {plan.TotalPlannedUpdates} schema file(s) across {modulesWithUpdates} module(s).");
        if (plan.TotalErrors > 0)
            preview.AppendLine($"{plan.TotalErrors} file(s) have no matching base schema and will be skipped, see below:");
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
        Theme.StyleContextMenu(contextMenu);
        var openFolderItem = new ToolStripMenuItem("Open containing folder");
        contextMenu.Items.Add(openFolderItem);
        contextMenu.Items.Add(new ToolStripSeparator());

        // The module(s) the "Set Load #" items act on, captured when the menu opens: the whole
        // selection if the right-clicked row is part of it, otherwise just the right-clicked row.
        var contextTargets = new List<ModuleInfo>();
        var passItems = new List<ToolStripMenuItem>();
        foreach (var pass in ModuleLayout.Passes)
        {
            var targetPass = pass;
            var item = new ToolStripMenuItem(PassItemText(targetPass, plural: false)) { Tag = targetPass };
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

        // Bottom of the menu: not about the clicked module(s) -- it re-sorts the active list.
        contextMenu.Items.Add(new ToolStripSeparator());
        var autosortItem = new ToolStripMenuItem("Autosort active modules");
        autosortItem.Click += (s, e) => RunAutosort();
        contextMenu.Items.Add(autosortItem);

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

            // With several modules selected the items act on all of them, and say so.
            var plural = contextTargets.Count > 1;
            openFolderItem.Text = plural ? "Open containing folders" : "Open containing folder";
            foreach (var item in passItems)
                item.Text = PassItemText((string)item.Tag!, plural);

            // Hide the Load # the module(s) are already in. With a multi-selection spanning several
            // Load #s an option stays visible as long as it would move at least one of them.
            foreach (var item in passItems)
            {
                var pass = (string)item.Tag!;
                item.Visible = contextTargets.Any(m => !string.Equals(m.LoadPass, pass, StringComparison.Ordinal));
            }
        };

        openFolderItem.Click += (s, e) =>
        {
            if (contextTargets.Count == 0) return;

            // Every selected module gets its own Explorer window, so guard against a stray huge selection.
            if (contextTargets.Count > MaxFolderWindowsWithoutAsking)
            {
                var answer = MessageBox.Show(this,
                    $"This will open {contextTargets.Count} Explorer windows. Continue?",
                    "Open Containing Folders", MessageBoxButtons.YesNo, MessageBoxIcon.Question, MessageBoxDefaultButton.Button2);
                if (answer != DialogResult.Yes) return;
            }

            foreach (var m in contextTargets)
                OpenModuleFolder(m.FullPath);
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

        /// Target Load # ("0".."4"); empty/invalid keeps the Load # the module is already in.
        public string Pass { get; set; } = "";
    }

    private const int MaxFolderWindowsWithoutAsking = 5;

    /// Right-click menu text for a Load # entry: "Set Load # to 2", or "Set Load #s to 2" when it
    /// will apply to several selected modules.
    private static string PassItemText(string pass, bool plural) =>
        $"Set Load #{(plural ? "s" : "")} to {ModuleLayout.PassDisplayName(pass)}";

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
    /// Returns false (and moves nothing) if the game is running and the user chose to abort.
    private bool PerformMoves(List<MoveRequest> requests)
    {
        if (requests.Count > 0 && !ConfirmGameNotRunning("Game Running",
                "The running game has already loaded its modules, so moving them now won't affect it until it is " +
                "restarted, and moving files the game has open can fail or cause problems.",
                "moving modules"))
        {
            lblStatus.Text = "Move aborted.";
            return false;
        }

        var errors = new List<string>();
        var pathErrors = new List<string>();
        foreach (var req in requests)
        {
            try
            {
                var src = req.Source.TrimEnd(Path.DirectorySeparatorChar, Path.AltDirectorySeparatorChar);
                var name = Path.GetFileName(src);

                // An unspecified Load # keeps the module in the Load # it's already in, which is what
                // preserves it when toggling active <-> inactive.
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
                               $"{(req.ToActive ? "active" : "inactive")} list ({ModuleLayout.PassLabel(ModuleLayout.GetPassFromPath(clash))}).");
                    continue;
                }

                var oldPass = ModuleLayout.GetPassFromPath(src);
                Directory.CreateDirectory(targetDir);
                Directory.Move(src, dest);

                // The module's own hardcoded "Modules/<Load #>/<name>/..." paths (art buttons etc.)
                // have to follow it to the new Load #. Silent unless something fails.
                if (!string.Equals(oldPass, pass, StringComparison.Ordinal))
                {
                    SetStatus($"Updating file paths in '{name}'...");
                    foreach (var e in ModulePathRewriter.Rewrite(dest, name, oldPass, pass))
                        pathErrors.Add($"{name}: {e}");
                }
            }
            catch (Exception ex)
            {
                errors.Add($"{Path.GetFileName(req.Source)}: {ex.Message}");
            }
        }

        if (errors.Count > 0 || pathErrors.Count > 0)
        {
            var text = new StringBuilder();
            if (errors.Count > 0)
            {
                text.AppendLine("Some modules couldn't be moved:\n");
                text.AppendLine(string.Join("\n", errors));
                text.AppendLine();
            }
            if (pathErrors.Count > 0)
            {
                text.AppendLine("These modules were moved, but some of their files couldn't be updated with the new Load #, " +
                                "so their art or other file paths may be broken:\n");
                text.AppendLine(string.Join("\n", pathErrors));
                text.AppendLine();
            }
            text.Append("If this keeps happening, try running the launcher as Administrator " +
                        "(this can happen when the game is installed under Program Files).");
            MessageBox.Show(this, text.ToString(), "Move Modules", MessageBoxButtons.OK, MessageBoxIcon.Warning);
        }

        // Other modules' references to the ones whose Load # just changed are fixed by the full scan,
        // at the next save / load / export / import / launch / refresh (see EnsureCrossModulePaths).

        RefreshModules();
        return true;
    }

    private void InstallDroppedModules(string[] droppedPaths, bool toActive)
    {
        // Modules dropped in from Explorer carry no Load # information, so they go in the default
        // Load # (1); right-click > Set Load # afterwards if they belong elsewhere.
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

    // ------------------------------------------- Cross-module path scan ---

    /// Status text describing what the last scan changed, or null if it changed nothing.
    private string? _lastScanSummary;

    /// Pairs ("A -> B") already reported by the inactive-reference notice this session, so the
    /// same notice doesn't come back on every launch/save/export. Refresh clears it.
    private readonly HashSet<string> _reportedInactiveRefs = new(StringComparer.OrdinalIgnoreCase);

    /// Sets the status bar text and repaints it immediately. Slow operations run on the UI thread, so
    /// without the forced repaint the text would not show until the work was over -- which is exactly
    /// when it is least useful (e.g. if something hangs).
    private void SetStatus(string text)
    {
        lblStatus.Text = text;
        lblStatus.Update();
    }

    /// Scans every module's XML (active and inactive) for paths into module folders and fixes the
    /// Load # in any that is wrong (see CrossModulePathScanner). Always runs when called: it is
    /// called by Save, Load, Export, Import, Launch and Refresh -- but not when modules are simply
    /// moved, to keep that fast -- so module files are consistent with where modules really are,
    /// even if folders were moved by hand. Takes well under a second on a typical install.
    /// Returns false only if something couldn't be updated AND the user chose to abort
    /// `abortAction` ("launching the game", ...); with a null `abortAction` problems are just
    /// reported and the caller carries on.
    private bool EnsureCrossModulePaths(string? abortAction)
    {
        _lastScanSummary = null;

        SetStatus("Checking module file paths...");
        Cursor = Cursors.WaitCursor;
        CrossModulePathScanner.ScanResult result;
        try
        {
            result = CrossModulePathScanner.Run(_modPath, SetStatus);
        }
        catch (Exception ex)
        {
            // Never leave the status stuck on "Checking...": report it like any other failure.
            result = new CrossModulePathScanner.ScanResult();
            result.Errors.Add($"The scan failed unexpectedly: {ex.Message}");
        }
        finally
        {
            Cursor = Cursors.Default;
        }

        if (result.ReferencesUpdated > 0)
        {
            _lastScanSummary = $"Updated {result.ReferencesUpdated} module path(s) in {result.FilesChanged} file(s) ({result.FilesScanned} XML files checked).";
            SetStatus(_lastScanSummary);
        }
        else if (result.Errors.Count == 0)
            SetStatus($"Module file paths are up to date ({result.FilesScanned} XML files checked).");
        else
            SetStatus("Checking module file paths had problems.");

        // Rewritten files can change a module's fingerprint, and with it whether a preset still matches.
        if (result.FilesChanged > 0)
        {
            RecomputeCurrentPreset();
            UpdateManageButton();
        }

        NotifyInactiveReferences(result);

        if (result.Errors.Count == 0) return true;

        var text = new StringBuilder();
        text.AppendLine("Some files couldn't be checked or updated, so paths in them that point into other modules " +
                        "may be wrong (art or other files may fail to load):");
        text.AppendLine();
        foreach (var err in result.Errors.Take(40)) text.AppendLine($"   - {err}");
        if (result.Errors.Count > 40) text.AppendLine($"   ... and {result.Errors.Count - 40} more");
        text.AppendLine();
        text.Append("If this keeps happening, try running the launcher as Administrator " +
                    "(this can happen when the game is installed under Program Files). The check runs again next time.");

        if (abortAction == null)
        {
            ShowScrollableMessage("Module File Paths", text.ToString());
            return true;
        }
        return ShowConfirmMessage("Module File Paths", text.ToString() + $"\n\nContinue anyway, or abort {abortAction}?",
            "Continue", "Abort", cancelIsDefault: true);
    }

    /// Tells the user about ACTIVE modules whose files point into modules that are only installed
    /// inactive. The paths are still kept up to date (so fingerprints stay consistent between
    /// machines), but the game can't find anything there while the other module is inactive, which
    /// usually means the author forgot to declare a dependency. Each pair is reported once per session.
    private void NotifyInactiveReferences(CrossModulePathScanner.ScanResult result)
    {
        var fresh = result.InactiveReferences
            .Where(r => _reportedInactiveRefs.Add($"{r.FromModule} -> {r.ToModule}"))
            .ToList();
        if (fresh.Count == 0) return;

        var byFolder = _activeModules.Concat(_inactiveModules)
            .GroupBy(m => m.FolderName, StringComparer.OrdinalIgnoreCase)
            .ToDictionary(g => g.Key, g => g.First(), StringComparer.OrdinalIgnoreCase);
        string Describe(string folder) => byFolder.TryGetValue(folder, out var m) ? DescribeModule(m) : $"'{folder}'";

        var text = new StringBuilder();
        text.AppendLine("Some active modules contain path references to modules that are currently inactive:");
        text.AppendLine();
        foreach (var group in fresh.GroupBy(r => r.FromModule, StringComparer.OrdinalIgnoreCase))
        {
            foreach (var r in group)
                text.AppendLine($"   - {Describe(r.FromModule)} references {Describe(r.ToModule)}, which is currently inactive.");
        }
        text.AppendLine();
        text.Append("This is likely due to a missing dependency, and may or may not cause issues " +
                    "(for example, missing art). This notice is shown once per session for each pair.");

        ShowScrollableMessage("Module Path References", text.ToString());
    }

    // ------------------------------------------------------------ Presets ---

    /// Labels the Delete and Load buttons for the selected preset -- Delete "Name" / Load "Name", the
    /// name cut with an ellipsis to fit the button -- and greys them out (unclickable) when there
    /// are no presets. The tooltips name the preset too.
    private void UpdatePresetButtons()
    {
        if (btnDeletePreset == null || btnLoadPreset == null) return;

        var name = cmbPresets.SelectedItem as string;
        var has = name != null;

        SetPresetButton(btnDeletePreset, "Delete", "Delete Preset", name);
        SetPresetButton(btnLoadPreset, "Load", "Load Preset", name);

        _presetToolTip.SetToolTip(btnDeletePreset, has
            ? $"Deletes the saved preset \"{name}\". Your modules are not touched."
            : "There are no saved presets to delete.");
        _presetToolTip.SetToolTip(btnLoadPreset, has
            ? $"Applies the saved preset \"{name}\": its modules are activated in their recorded Load #s and all other modules are deactivated."
            : "There are no saved presets to load.");
    }

    private static void SetPresetButton(Button button, string verb, string idleText, string? name)
    {
        if (name == null)
        {
            button.Text = idleText;
            button.Enabled = false;
            return;
        }

        var maxWidth = button.Width - Theme.S(16);
        int Measure(string t) => TextRenderer.MeasureText(t, button.Font, Size.Empty,
            TextFormatFlags.NoPadding | TextFormatFlags.SingleLine).Width;

        var shown = name;
        while (shown.Length > 1 && Measure($"{verb} \"{shown}\"") > maxWidth)
            shown = shown.Substring(0, shown.Length - 1);
        button.Text = shown.Length < name.Length ? $"{verb} \"{shown.TrimEnd()}\u2026\"" : $"{verb} \"{name}\"";
        button.Enabled = true;
    }

    private void RefreshPresetCombo(bool updateManageButton = true)
    {
        cmbPresets.Items.Clear();
        foreach (var p in _config.Presets.OrderBy(p => p.Name, StringComparer.OrdinalIgnoreCase))
            cmbPresets.Items.Add(p.Name);
        if (cmbPresets.Items.Count > 0) cmbPresets.SelectedIndex = 0;
        UpdatePresetButtons();
        if (updateManageButton)
        {
            RecomputeCurrentPreset();
            UpdateManageButton();
        }
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

        var name = InputForm.Prompt(this, "Save Preset", $"Preset name (up to {MaxPresetNameLength} characters):", "",
            maxLength: MaxPresetNameLength);
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

        // With Futureproof checked the preset is saved as if it were an imported futureproof code: no
        // versions or fingerprints, so loading it only checks that each module is installed.
        var futureproof = chkFutureproof.Checked;

        // Fingerprints are about to be recorded: make sure modules' paths into other modules are current first.
        if (!futureproof && !EnsureCrossModulePaths("saving the preset"))
            return;

        Cursor = Cursors.WaitCursor;
        var preset = new Preset { Name = name, SourceVersion = ReadModVersion() };
        foreach (var m in _activeModules)
        {
            if (!futureproof) SetStatus($"Fingerprinting '{m.Name}'...");
            preset.Modules.Add(new ModuleRef
            {
                Name = m.FolderName,
                Version = futureproof ? "" : m.Version,
                Fingerprint = futureproof ? "" : ModuleScanner.ComputeFingerprint(m.FullPath),
                LoadPass = m.LoadPass,
            });
        }
        Cursor = Cursors.Default;

        _config.Presets.Add(preset);
        SaveConfig();
        RefreshPresetCombo();
        cmbPresets.SelectedItem = preset.Name;
        lblStatus.Text = $"Saved preset '{preset.Name}' with {preset.Modules.Count} modules{(futureproof ? " (futureproof)" : "")}.";
    }

    private void LoadPreset()
    {
        var preset = GetSelectedPreset();
        if (preset == null) return;
        ApplyPreset(preset);
    }

    /// Moves modules to match the preset, runs the cross-module path scan, THEN compares fingerprints,
    /// so they reflect the folders as they are on disk after the moves.
    private void ApplyPreset(Preset preset)
    {
        var wanted = preset.Modules
            .GroupBy(m => m.Name, StringComparer.OrdinalIgnoreCase)
            .ToDictionary(g => g.Key, g => g.First(), StringComparer.OrdinalIgnoreCase);

        var beforeCurrent = _activeModules.Concat(_inactiveModules)
            .GroupBy(m => m.FolderName, StringComparer.OrdinalIgnoreCase)
            .ToDictionary(g => g.Key, g => g.First(), StringComparer.OrdinalIgnoreCase);

        var missing = preset.Modules.Where(m => !beforeCurrent.ContainsKey(m.Name)).ToList();

        // Wanted modules end up active in the Load # the preset recorded (a module with no recorded
        // Load # stays in its current one); unwanted active modules are deactivated, keeping their Load #.
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
        if (requests.Count > 0 && !PerformMoves(requests))
        {
            Cursor = Cursors.Default;
            lblStatus.Text = $"Applying preset '{preset.Name}' aborted.";
            return;
        }

        // The preset may have moved modules to other Load #s, so paths in other modules' XML that
        // point at them can be stale and would make the fingerprints below differ for no real reason.
        EnsureCrossModulePaths(abortAction: null);

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
        var checkedCount = 0;
        foreach (var pm in preset.Modules)
        {
            if (afterCurrent.TryGetValue(pm.Name, out var local) && !string.IsNullOrEmpty(pm.Fingerprint))
            {
                SetStatus($"Comparing modules with the preset ({++checkedCount}): {local.Name}...");
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

        SetStatus($"Applied preset '{preset.Name}'.");
        if (msg.Length > 0)
            ShowScrollableMessage($"Applied Preset: {preset.Name}", msg.ToString());
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

    /// Exports the CURRENT active modules (not a saved preset) as a share code: each module's folder
    /// name and Load #, plus version and content fingerprint unless Futureproof is checked. If the
    /// active modules exactly match a saved preset, its name is put in the code's id string.
    private void ExportPreset()
    {
        // Re-read the disk first: modules may have been moved by hand since the last refresh.
        RefreshModules();

        if (!VerifyActiveModules("exporting the active modules"))
            return;

        // Scan first: the fingerprints in the code must describe the module files exactly as they
        // are on disk right now.
        if (!EnsureCrossModulePaths("exporting the active modules"))
            return;

        Cursor = Cursors.WaitCursor;
        var fingerprints = new Dictionary<string, string>(StringComparer.OrdinalIgnoreCase);
        var preset = new Preset { SourceVersion = ReadModVersion() };
        foreach (var m in _activeModules.OrderBy(m => m.FolderName, StringComparer.OrdinalIgnoreCase))
        {
            SetStatus($"Fingerprinting '{m.Name}'...");
            var fp = ModuleScanner.ComputeFingerprint(m.FullPath);
            fingerprints[m.FolderName] = fp;
            preset.Modules.Add(new ModuleRef { Name = m.FolderName, Version = m.Version, Fingerprint = fp, LoadPass = m.LoadPass });
        }
        var matchingName = FindMatchingPresetName(fingerprints);
        preset.Name = matchingName ?? "";
        Cursor = Cursors.Default;

        var futureproof = chkFutureproof.Checked;
        var code = PresetCodec.Encode(preset, futureproof, ReadModVersion());
        Clipboard.SetText(code);
        SetStatus($"Copied a preset code for {preset.Modules.Count} active modules to the clipboard.");

        var overLimit = code.Length > PresetCodec.DiscordSafeLimit;
        var warning = overLimit
            ? $"\n\nHeads up: this code is {code.Length} characters, over Discord's 2000-character message limit. " +
              (futureproof ? "Try deactivating some modules." : "Try the Futureproof option to shrink it, or deactivate some modules.")
            : "";
        var named = matchingName != null ? $" It is labelled with your saved preset '{matchingName}', which these modules match." : "";

        MessageBox.Show(this,
            $"Your {preset.Modules.Count} active modules were copied to your clipboard as a share code ({code.Length} characters).{named}{warning}",
            "Export Active Modules", MessageBoxButtons.OK, overLimit ? MessageBoxIcon.Warning : MessageBoxIcon.Information);
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

        var suggested = preset.Name.Length > MaxPresetNameLength ? preset.Name.Substring(0, MaxPresetNameLength) : preset.Name;
        var name = InputForm.PromptWithAlternate(this, "Name This Preset",
            $"Save the imported preset as (up to {MaxPresetNameLength} characters):", suggested,
            "Don't save", out var dontSave, maxLength: MaxPresetNameLength);

        if (dontSave)
        {
            // Keep the code out of the saved presets, but still offer to apply it.
            preset.Name = suggested.Trim().Length > 0 ? suggested.Trim() : "Imported preset";
        }
        else
        {
            if (string.IsNullOrWhiteSpace(name)) return;
            preset.Name = name!.Trim();

            var existing = _config.Presets.FirstOrDefault(p => p.Name.Equals(preset.Name, StringComparison.OrdinalIgnoreCase));
            if (existing != null) _config.Presets.Remove(existing);

            _config.Presets.Add(preset);
            SaveConfig();
            RefreshPresetCombo();
            cmbPresets.SelectedItem = preset.Name;
        }

        var localVersion = ReadModVersion();
        var versionNote = (!string.IsNullOrEmpty(preset.SourceVersion) &&
                            !string.Equals(preset.SourceVersion, localVersion, StringComparison.OrdinalIgnoreCase))
            ? $"\n\nNote: this preset was exported from AoE v{preset.SourceVersion}; you're running v{localVersion}."
            : "";

        var apply = MessageBox.Show(this,
            $"Preset '{preset.Name}' imported with {preset.Modules.Count} modules{(dontSave ? " (not saved)" : "")}.{versionNote}\n\nApply it now?",
            "Import Preset", MessageBoxButtons.YesNo, MessageBoxIcon.Question);
        if (apply == DialogResult.Yes)
            ApplyPreset(preset);
    }
}
