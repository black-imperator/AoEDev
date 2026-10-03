using System.Drawing;
using System.Windows.Forms;

namespace AoELauncher.UI;

/// <summary>
/// Dark grey / white / orange color scheme, matching the original AoE
/// launcher's look. Native WinForms GroupBox borders remain OS-themed
/// (they don't fully recolor without owner-drawing the control), so those
/// may look slightly off against the dark background -- everything else
/// (fills, text, buttons, grids) is fully themed.
/// </summary>
public static class Theme
{
    public static readonly Color Background = Color.FromArgb(37, 37, 38);
    public static readonly Color Panel = Color.FromArgb(45, 45, 48);
    public static readonly Color ControlBack = Color.FromArgb(60, 60, 63);
    public static readonly Color Text = Color.FromArgb(240, 240, 240);
    public static readonly Color MutedText = Color.FromArgb(180, 180, 180);
    public static readonly Color Accent = Color.FromArgb(230, 126, 34);
    public static readonly Color GridLine = Color.FromArgb(70, 70, 74);

    /// <summary>Uniform height applied to every button in the app except the large Launch button.</summary>
    public const int ButtonHeight = 30;

    public static void StyleForm(Form form)
    {
        form.BackColor = Background;
        form.ForeColor = Text;
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
