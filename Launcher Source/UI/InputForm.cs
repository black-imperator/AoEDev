using System;
using System.Drawing;
using System.Windows.Forms;

namespace AoELauncher.UI;

public class InputForm : Form
{
    private readonly TextBox _textBox;
    public string Value => _textBox.Text;

    /// True if the user pressed the extra (alternate) button instead of OK or Cancel.
    public bool AlternateChosen { get; private set; }

    private InputForm(string title, string label, string initial, bool multiline, int maxLength, string? alternateText)
    {
        Text = title;
        ClientSize = new Size(Theme.S(460), Theme.S(200));
        StartPosition = FormStartPosition.CenterParent;
        FormBorderStyle = FormBorderStyle.FixedDialog;
        MaximizeBox = false;
        MinimizeBox = false;
        Theme.StyleForm(this);

        var lbl = new Label { Text = label, Left = Theme.S(12), Top = Theme.S(12), Width = Theme.S(420), Height = Theme.BodyFont.Height + Theme.S(6) };
        Theme.StyleLabel(lbl);
        Controls.Add(lbl);

        _textBox = new TextBox
        {
            Left = Theme.S(12),
            Top = Theme.S(12) + Theme.BodyFont.Height + Theme.S(14),
            Width = Theme.S(420),
            Multiline = multiline,
            Height = multiline ? Theme.S(150) : Theme.BodyFont.Height + Theme.S(8),
            ScrollBars = multiline ? ScrollBars.Vertical : ScrollBars.None,
            Text = initial,
        };
        if (maxLength > 0) _textBox.MaxLength = maxLength;
        Theme.StyleTextBox(_textBox);
        Controls.Add(_textBox);

        var buttonTop = _textBox.Bottom + Theme.S(12);
        var okBtn = new FlatButton { Text = "OK", DialogResult = DialogResult.OK, Left = Theme.S(264), Width = Theme.S(80), Height = Theme.ButtonHeight, Top = buttonTop };
        var cancelBtn = new FlatButton { Text = "Cancel", DialogResult = DialogResult.Cancel, Left = Theme.S(352), Width = Theme.S(80), Height = Theme.ButtonHeight, Top = buttonTop };
        Theme.StyleButton(okBtn, primary: true);
        Theme.StyleButton(cancelBtn);
        Controls.Add(okBtn);
        Controls.Add(cancelBtn);

        // Optional third button between OK and Cancel; OK and the alternate shift left to make room.
        if (alternateText != null)
        {
            var altWidth = Math.Max(Theme.S(80), TextRenderer.MeasureText(alternateText, Theme.BodyFont).Width + Theme.S(24));
            var altBtn = new FlatButton { Text = alternateText, Width = altWidth, Height = Theme.ButtonHeight, Top = buttonTop };
            altBtn.Left = cancelBtn.Left - Theme.S(8) - altWidth;
            okBtn.Left = altBtn.Left - Theme.S(8) - okBtn.Width;
            Theme.StyleButton(altBtn);
            altBtn.Click += (s, e) =>
            {
                AlternateChosen = true;
                DialogResult = DialogResult.OK;
            };
            Controls.Add(altBtn);
        }

        AcceptButton = okBtn;
        CancelButton = cancelBtn;

        ClientSize = new Size(ClientSize.Width, _textBox.Bottom + Theme.S(12) + Theme.ButtonHeight + Theme.S(14));
    }

    /// `maxLength` > 0 limits how much can be typed or pasted.
    public static string? Prompt(IWin32Window owner, string title, string label, string initial,
        bool multiline = false, int maxLength = 0)
    {
        using var form = new InputForm(title, label, initial, multiline, maxLength, null);
        return form.ShowDialog(owner) == DialogResult.OK ? form.Value : null;
    }

    /// Like Prompt, with an extra button between OK and Cancel. If it is pressed, `alternate` is true
    /// and the result is null.
    public static string? PromptWithAlternate(IWin32Window owner, string title, string label, string initial,
        string alternateText, out bool alternate, int maxLength = 0)
    {
        using var form = new InputForm(title, label, initial, false, maxLength, alternateText);
        var result = form.ShowDialog(owner);
        alternate = result == DialogResult.OK && form.AlternateChosen;
        return result == DialogResult.OK && !alternate ? form.Value : null;
    }
}
