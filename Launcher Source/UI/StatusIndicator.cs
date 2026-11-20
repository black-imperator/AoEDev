using System;
using System.Collections.Generic;
using System.Drawing;
using System.Linq;
using System.Windows.Forms;

namespace AoELauncher.UI;

/// Single-line "Status: <value>" readout, centered in the control, with the value drawn in its
/// own (bold) color. A plain Label can only have one text color, hence the custom paint.
public class StatusIndicator : Control
{
    private const string Prefix = "Status: ";
    private const TextFormatFlags Flags =
        TextFormatFlags.NoPadding | TextFormatFlags.SingleLine | TextFormatFlags.NoPrefix |
        TextFormatFlags.VerticalCenter | TextFormatFlags.Left;

    private readonly Font _valueFont = new(Theme.BodyFont, FontStyle.Bold);
    private string _value = "";
    private Color _valueColor = Theme.Text;

    public StatusIndicator()
    {
        SetStyle(ControlStyles.UserPaint | ControlStyles.AllPaintingInWmPaint |
                 ControlStyles.OptimizedDoubleBuffer | ControlStyles.ResizeRedraw, true);
        TabStop = false;
        BackColor = Theme.Panel;
        ForeColor = Theme.Text;
        Font = Theme.BodyFont;
    }

    public string Value => _value;

    public void SetStatus(string value, Color color)
    {
        if (_value == value && _valueColor == color) return;
        _value = value;
        _valueColor = color;
        Invalidate();
    }

    /// Width needed to show "Status: <value>" for the widest of the given values.
    public int MeasureWidth(IEnumerable<string> possibleValues)
    {
        var prefixWidth = TextRenderer.MeasureText(Prefix, Theme.BodyFont, Size.Empty, Flags).Width;
        var valueWidth = possibleValues.Max(v => TextRenderer.MeasureText(v, _valueFont, Size.Empty, Flags).Width);
        return prefixWidth + valueWidth + Theme.S(8);
    }

    protected override void OnPaint(PaintEventArgs e)
    {
        e.Graphics.Clear(BackColor);

        var prefixSize = TextRenderer.MeasureText(e.Graphics, Prefix, Theme.BodyFont, Size.Empty, Flags);
        var valueSize = TextRenderer.MeasureText(e.Graphics, _value, _valueFont, Size.Empty, Flags);

        var x = Math.Max(0, (Width - (prefixSize.Width + valueSize.Width)) / 2);
        TextRenderer.DrawText(e.Graphics, Prefix, Theme.BodyFont,
            new Rectangle(x, 0, prefixSize.Width, Height), Theme.Text, Flags);
        TextRenderer.DrawText(e.Graphics, _value, _valueFont,
            new Rectangle(x + prefixSize.Width, 0, valueSize.Width, Height), _valueColor, Flags);
    }

    protected override void Dispose(bool disposing)
    {
        if (disposing) _valueFont.Dispose();
        base.Dispose(disposing);
    }
}
