using System;
using System.Drawing;
using System.Windows.Forms;

namespace AoELauncher.UI;

public enum TagFilterState
{
    /// No filtering on this tag.
    Neutral,

    /// Modules WITHOUT this tag are filtered out.
    Whitelist,

    /// Modules WITH this tag are filtered out.
    Blacklist,
}

/// A tag name followed by a small three-state box: empty (neutral), white (whitelist) or black
/// (blacklist). Left-click cycles neutral -> whitelist -> blacklist -> neutral; right-click
/// clears it back to neutral. WinForms' own CheckBox can be three-state, but its "indeterminate"
/// look is a gray square that can't tell two meanings apart, so this draws its own box.
public class TagFilterBox : Control
{
    private static readonly int BoxSize = Theme.S(14);
    private static readonly int Gap = Theme.S(4); // label-to-box gap
    private const TextFormatFlags TextFlags =
        TextFormatFlags.Left | TextFormatFlags.VerticalCenter | TextFormatFlags.NoPadding | TextFormatFlags.SingleLine;

    private bool _hover;

    public TagFilterState State { get; private set; } = TagFilterState.Neutral;

    /// Raised whenever the state changes (by click or via SetState).
    public event EventHandler? StateChanged;

    public TagFilterBox()
    {
        SetStyle(ControlStyles.UserPaint | ControlStyles.AllPaintingInWmPaint |
                 ControlStyles.OptimizedDoubleBuffer | ControlStyles.ResizeRedraw, true);
        SetStyle(ControlStyles.Selectable, false); // clicking it shouldn't take keyboard focus away from the lists
        BackColor = Theme.Panel;
        ForeColor = Theme.Text;
        Font = Theme.BodyFont;
        Cursor = Cursors.Hand;
        TabStop = false;
    }

    /// Sizes the control to fit its text plus the box.
    public void FitToText()
    {
        var textWidth = TextRenderer.MeasureText(Text, Font, Size.Empty, TextFlags).Width;
        Size = new Size(textWidth + Gap + BoxSize + 2, Math.Max(Theme.S(22), Font.Height + Theme.S(6)));
    }

    public void SetState(TagFilterState state)
    {
        if (State == state) return;
        State = state;
        Invalidate();
        StateChanged?.Invoke(this, EventArgs.Empty);
    }

    protected override void OnMouseClick(MouseEventArgs e)
    {
        base.OnMouseClick(e);
        if (e.Button == MouseButtons.Left)
        {
            SetState(State switch
            {
                TagFilterState.Neutral => TagFilterState.Whitelist,
                TagFilterState.Whitelist => TagFilterState.Blacklist,
                _ => TagFilterState.Neutral,
            });
        }
        else if (e.Button == MouseButtons.Right)
        {
            SetState(TagFilterState.Neutral);
        }
    }

    protected override void OnMouseEnter(EventArgs e) { base.OnMouseEnter(e); _hover = true; Invalidate(); }
    protected override void OnMouseLeave(EventArgs e) { base.OnMouseLeave(e); _hover = false; Invalidate(); }

    protected override void OnPaint(PaintEventArgs e)
    {
        var g = e.Graphics;
        g.Clear(BackColor);

        var textWidth = TextRenderer.MeasureText(Text, Font, Size.Empty, TextFlags).Width;
        TextRenderer.DrawText(g, Text, Font, new Rectangle(0, 0, textWidth, Height), ForeColor, TextFlags);

        var box = new Rectangle(textWidth + Gap, (Height - BoxSize) / 2, BoxSize, BoxSize);
        var fill = State switch
        {
            TagFilterState.Whitelist => Color.White,
            TagFilterState.Blacklist => Color.Black,
            _ => Theme.ControlBack,
        };
        using (var brush = new SolidBrush(fill))
            g.FillRectangle(brush, box);
        // A light border keeps the black state visible against the dark background.
        using (var pen = new Pen(_hover ? Theme.Accent : Theme.MutedText))
            g.DrawRectangle(pen, box.X, box.Y, box.Width - 1, box.Height - 1);
    }
}
