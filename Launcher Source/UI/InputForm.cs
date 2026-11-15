using System.Drawing;
using System.Windows.Forms;

namespace AoELauncher.UI;

public class InputForm : Form
{
    private readonly TextBox _textBox;
    public string Value => _textBox.Text;

    private InputForm(string title, string label, string initial, bool multiline)
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
        Theme.StyleTextBox(_textBox);
        Controls.Add(_textBox);

        var okBtn = new FlatButton { Text = "OK", DialogResult = DialogResult.OK, Left = Theme.S(264), Width = Theme.S(80), Height = Theme.ButtonHeight, Top = _textBox.Bottom + Theme.S(12) };
        var cancelBtn = new FlatButton { Text = "Cancel", DialogResult = DialogResult.Cancel, Left = Theme.S(352), Width = Theme.S(80), Height = Theme.ButtonHeight, Top = _textBox.Bottom + Theme.S(12) };
        Theme.StyleButton(okBtn, primary: true);
        Theme.StyleButton(cancelBtn);
        Controls.Add(okBtn);
        Controls.Add(cancelBtn);
        AcceptButton = okBtn;
        CancelButton = cancelBtn;

        ClientSize = new Size(ClientSize.Width, _textBox.Bottom + Theme.S(12) + Theme.ButtonHeight + Theme.S(14));
    }

    public static string? Prompt(IWin32Window owner, string title, string label, string initial, bool multiline = false)
    {
        using var form = new InputForm(title, label, initial, multiline);
        return form.ShowDialog(owner) == DialogResult.OK ? form.Value : null;
    }
}
