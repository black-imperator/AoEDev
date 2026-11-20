using System.Drawing;
using System.Windows.Forms;

namespace AoELauncher.UI;

/// A plain WinForms Button shows a dotted focus-cue rectangle once it's been
/// clicked, and that rectangle stays visible until some other control takes
/// focus -- which reads as an extra "bolded" border that doesn't go away.
/// Overriding ShowFocusCues is the standard, documented way to suppress
/// just that visual cue without otherwise changing button behavior.
///
/// A disabled flat button is also drawn explicitly: grey text on the normal background with a
/// grey border, because the stock disabled rendering is hard to read on the dark theme.
public class FlatButton : Button
{
    private static readonly Color DisabledText = Color.FromArgb(120, 120, 120);
    private static readonly Color DisabledBorder = Color.FromArgb(80, 80, 84);

    protected override bool ShowFocusCues => false;

    protected override void OnPaint(PaintEventArgs pevent)
    {
        base.OnPaint(pevent);
        if (Enabled) return;

        var g = pevent.Graphics;
        using (var back = new SolidBrush(BackColor))
            g.FillRectangle(back, ClientRectangle);
        using (var pen = new Pen(DisabledBorder))
            g.DrawRectangle(pen, 0, 0, Width - 1, Height - 1);
        TextRenderer.DrawText(g, Text, Font, ClientRectangle, DisabledText,
            TextFormatFlags.HorizontalCenter | TextFormatFlags.VerticalCenter |
            TextFormatFlags.EndEllipsis | TextFormatFlags.NoPadding);
    }

    protected override void OnEnabledChanged(System.EventArgs e)
    {
        base.OnEnabledChanged(e);
        Invalidate();
    }
}
