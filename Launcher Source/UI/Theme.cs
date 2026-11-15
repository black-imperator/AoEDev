using System;
using System.Drawing;
using System.Windows.Forms;

namespace AoELauncher.UI;

/// Dark grey / white / orange color scheme, matching the original AoE
/// launcher's look. Native WinForms GroupBox borders remain OS-themed
/// (they don't fully recolor without owner-drawing the control), so those
/// may look slightly off against the dark background -- everything else
/// (fills, text, buttons, grids) is fully themed.
public static class Theme
{
    public static readonly Color Background = Color.FromArgb(37, 37, 38);
    public static readonly Color Panel = Color.FromArgb(45, 45, 48);
    public static readonly Color ControlBack = Color.FromArgb(60, 60, 63);
    public static readonly Color Text = Color.FromArgb(240, 240, 240);
    public static readonly Color MutedText = Color.FromArgb(180, 180, 180);
    public static readonly Color Accent = Color.FromArgb(230, 126, 34);
    public static readonly Color GridLine = Color.FromArgb(70, 70, 74);

    // Rows of modules that don't match the tag filters are shown greyed out.
    public static readonly Color FilteredText = Color.FromArgb(120, 120, 124);
    public static readonly Color FilteredSelectionBack = Color.FromArgb(105, 78, 50);
    public static readonly Color FilteredSelectionText = Color.FromArgb(190, 190, 190);

    /// Global UI scale. Body text is FontScale x the system default font size; pixel sizes
    /// (button widths, paddings, column widths...) go through S() so layout follows the text.
    /// Change this one number to make the whole UI bigger or smaller.
    public const float FontScale = 1.5f;

    /// Titles/headings grow less than body text (they were already large).
    public const float TitleScale = 1.2f;

    /// Scales a design-time pixel value by FontScale.
    public static int S(int px) => (int)Math.Round(px * FontScale);

    /// The app-wide body font: the system default UI font at FontScale x its size.
    public static readonly Font BodyFont =
        new Font(Control.DefaultFont.FontFamily, Control.DefaultFont.Size * FontScale, FontStyle.Regular);

    /// A bold heading font, a bit larger than body text. 'relativeToBody' is a multiple of the body size.
    public static Font HeadingFont(float relativeToBody) =>
        new Font(BodyFont.FontFamily, BodyFont.Size * relativeToBody, FontStyle.Bold);

    /// Uniform height applied to every button in the app except the large Launch button.
    public static readonly int ButtonHeight = 42;

    public static void StyleForm(Form form)
    {
        form.AutoScaleMode = AutoScaleMode.None;
        form.Font = BodyFont;
        form.BackColor = Background;
        form.ForeColor = Text;
    }

    /// Tooltips ignore the form's font unless owner-drawn, so draw them ourselves at body size.
    /// 'currentText' is needed for tips shown via ToolTip.Show(), where GetToolTip() has no text to return.
    public static void StyleToolTip(ToolTip tip, int maxWidth = 640, Func<string>? currentText = null)
    {
        tip.OwnerDraw = true;
        var flags = TextFormatFlags.WordBreak | TextFormatFlags.NoPadding | TextFormatFlags.Left | TextFormatFlags.Top;
        int pad = S(6);
        tip.Popup += (s, e) =>
        {
            var tipText = currentText != null ? currentText() : tip.GetToolTip(e.AssociatedControl);
            var size = TextRenderer.MeasureText(tipText, BodyFont, new Size(maxWidth, 0), flags);
            e.ToolTipSize = new Size(size.Width + pad * 2, size.Height + pad * 2);
        };
        tip.Draw += (s, e) =>
        {
            using (var back = new SolidBrush(ControlBack)) e.Graphics.FillRectangle(back, e.Bounds);
            using (var pen = new Pen(Accent)) e.Graphics.DrawRectangle(pen, 0, 0, e.Bounds.Width - 1, e.Bounds.Height - 1);
            var rect = new Rectangle(pad, pad, e.Bounds.Width - pad * 2, e.Bounds.Height - pad * 2);
            TextRenderer.DrawText(e.Graphics, e.ToolTipText, BodyFont, rect, Text, flags);
        };
    }

    public static void StyleContainer(Control control)
    {
        control.BackColor = Panel;
        control.ForeColor = Text;
    }

    public static void StyleButton(Button button, bool primary = false)
    {
        button.FlatStyle = FlatStyle.Flat;
        button.BackColor = ControlBack;
        button.ForeColor = Text;
        button.FlatAppearance.BorderColor = Accent;
        button.FlatAppearance.BorderSize = primary ? 2 : 1;
        button.FlatAppearance.MouseOverBackColor = Color.FromArgb(75, 75, 79);
        button.FlatAppearance.MouseDownBackColor = Color.FromArgb(85, 65, 40);
    }

    public static void StyleTextBox(TextBox box)
    {
        box.BackColor = ControlBack;
        box.ForeColor = Text;
        box.BorderStyle = BorderStyle.FixedSingle;
    }

    public static void StyleComboBox(ComboBox box)
    {
        box.FlatStyle = FlatStyle.Flat;
        box.BackColor = ControlBack;
        box.ForeColor = Text;
    }

    public static void StyleLabel(Label label, bool muted = false)
    {
        label.ForeColor = muted ? MutedText : Text;
        label.BackColor = Color.Transparent;
    }

    public static void StyleCheckBox(CheckBox box)
    {
        box.ForeColor = Text;
        box.BackColor = Color.Transparent;
    }

    public static void StyleGrid(DataGridView grid)
    {
        grid.BackgroundColor = Panel;
        grid.GridColor = GridLine;
        grid.EnableHeadersVisualStyles = false;

        grid.ColumnHeadersDefaultCellStyle.BackColor = ControlBack;
        grid.ColumnHeadersDefaultCellStyle.ForeColor = Text;
        grid.ColumnHeadersDefaultCellStyle.SelectionBackColor = ControlBack;
        grid.ColumnHeadersDefaultCellStyle.SelectionForeColor = Text;
        grid.ColumnHeadersBorderStyle = DataGridViewHeaderBorderStyle.Single;

        grid.DefaultCellStyle.BackColor = Panel;
        grid.DefaultCellStyle.ForeColor = Text;
        grid.DefaultCellStyle.SelectionBackColor = Accent;
        grid.DefaultCellStyle.SelectionForeColor = Color.Black;

        grid.RowsDefaultCellStyle.BackColor = Panel;
        grid.RowsDefaultCellStyle.ForeColor = Text;
        grid.AlternatingRowsDefaultCellStyle.BackColor = Color.FromArgb(50, 50, 53);
        grid.AlternatingRowsDefaultCellStyle.ForeColor = Text;
    }
}
