using System;
using System.Runtime.InteropServices;
using System.Windows.Forms;

namespace AoELauncher.UI;

/// <summary>
/// A read-only, multiline TextBox used for the app's report/message
/// dialogs. Fixes two standard WinForms annoyances for this use case:
///   1. A TextBox that's the first (or only) focusable control on a newly
///      shown dialog gets its entire contents auto-selected/highlighted.
///   2. Any focused TextBox shows a blinking caret, which looks odd on a
///      control that's meant to be read-only report text, not an input
///      field -- even though selecting and Ctrl+C copying text is still
///      fully supported and desired.
/// Both are fixed by resetting selection and hiding the caret whenever
/// focus/click/key events could show or reset them; HideCaret only affects
/// the blinking caret's visibility, not the underlying selection or
/// keyboard/mouse interaction, so drag-to-select and copy keep working
/// normally.
/// </summary>
public class ReadOnlySelectableTextBox : TextBox
{
    [DllImport("user32.dll")]
    private static extern bool HideCaret(IntPtr hWnd);

    public ReadOnlySelectableTextBox()
    {
        ReadOnly = true;
        Multiline = true;
    }

    protected override void OnGotFocus(EventArgs e)
    {
        base.OnGotFocus(e);
        Select(0, 0); // undo WinForms' automatic "select all" on first focus
        HideCaret(Handle);
    }

    protected override void OnMouseDown(MouseEventArgs e)
    {
        base.OnMouseDown(e);
        HideCaret(Handle);
    }

    protected override void OnMouseUp(MouseEventArgs e)
    {
        base.OnMouseUp(e);
        HideCaret(Handle);
    }

    protected override void OnKeyDown(KeyEventArgs e)
    {
        base.OnKeyDown(e);
        HideCaret(Handle);
    }
}
