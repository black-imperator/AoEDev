using System.Windows.Forms;

namespace AoELauncher.UI;

public class InputForm : Form
{
    private readonly TextBox _textBox;
    public string Value => _textBox.Text;

    private InputForm(string title, string label, string initial, bool multiline)
    {
        Text = title;
        Width = 460;
        StartPosition = FormStartPosition.CenterParent;
        FormBorderStyle = FormBorderStyle.FixedDialog;
        MaximizeBox = false;
        MinimizeBox = false;
        Theme.StyleForm(this);

        var lbl = new Label { Text = label, Left = 12, Top = 12, Width = 420 };
        Theme.StyleLabel(lbl);
        Controls.Add(lbl);

        _textBox = new TextBox
        {
            Left = 12,
            Top = 36,
            Width = 420,
            Multiline = multiline,
            Height = multiline ? 150 : 24,
            ScrollBars = multiline ? ScrollBars.Vertical : ScrollBars.None,
            Text = initial,
        };
        Theme.StyleTextBox(_textBox);
        Controls.Add(_textBox);

        var okBtn = new FlatButton { Text = "OK", DialogResult = DialogResult.OK, Left = 264, Width = 80, Height = Theme.ButtonHeight, Top = _textBox.Bottom + 12 };
        var cancelBtn = new FlatButton { Text = "Cancel", DialogResult = DialogResult.Cancel, Left = 352, Width = 80, Height = Theme.ButtonHeight, Top = _textBox.Bottom + 12 };
        Theme.StyleButton(okBtn, primary: true);
        Theme.StyleButton(cancelBtn);
        Controls.Add(okBtn);
        Controls.Add(cancelBtn);
        AcceptButton = okBtn;
        CancelButton = cancelBtn;

        Height = _textBox.Bottom + 90;
    }

    public static string? Prompt(IWin32Window owner, string title, string label, string initial, bool multiline = false)
    {
        using var form = new InputForm(title, label, initial, multiline);
        return form.ShowDialog(owner) == DialogResult.OK ? form.Value : null;
    }
}
