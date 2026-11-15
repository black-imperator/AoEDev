using System.Drawing;
using System.Windows.Forms;

namespace AoELauncher.UI;

public enum PlacementChoice
{
    Recheck,
    ContinueAnyway,
    Quit,
}

public class PlacementIssuesForm : Form
{
    public PlacementChoice Choice { get; private set; } = PlacementChoice.Quit;

    public PlacementIssuesForm(string message)
    {
        Text = "Setup Check";
        ClientSize = new Size(Theme.S(580), Theme.S(430));
        StartPosition = FormStartPosition.CenterParent;
        FormBorderStyle = FormBorderStyle.FixedDialog;
        MaximizeBox = false;
        MinimizeBox = false;
        Theme.StyleForm(this);

        var box = new ReadOnlySelectableTextBox
        {
            Left = Theme.S(12), Top = Theme.S(12), Width = Theme.S(540), Height = Theme.S(300),
            ScrollBars = ScrollBars.Vertical,
            Text = message,
        };
        Theme.StyleTextBox(box);
        Controls.Add(box);

        var buttonsTop = box.Bottom + Theme.S(16);
        var btnRecheck = new FlatButton { Text = "Re-check", Left = Theme.S(12), Top = buttonsTop, Width = Theme.S(150), Height = Theme.ButtonHeight };
        var btnContinue = new FlatButton { Text = "Continue Anyway", Left = Theme.S(172), Top = buttonsTop, Width = Theme.S(190), Height = Theme.ButtonHeight };
        var btnQuit = new FlatButton { Text = "Quit", Left = Theme.S(428), Top = buttonsTop, Width = Theme.S(124), Height = Theme.ButtonHeight };
        Theme.StyleButton(btnRecheck, primary: true);
        Theme.StyleButton(btnContinue);
        Theme.StyleButton(btnQuit);

        btnRecheck.Click += (s, e) => { Choice = PlacementChoice.Recheck; DialogResult = DialogResult.OK; };
        btnContinue.Click += (s, e) => { Choice = PlacementChoice.ContinueAnyway; DialogResult = DialogResult.OK; };
        btnQuit.Click += (s, e) => { Choice = PlacementChoice.Quit; DialogResult = DialogResult.Cancel; };

        Controls.Add(btnRecheck);
        Controls.Add(btnContinue);
        Controls.Add(btnQuit);
        CancelButton = btnQuit;

        ClientSize = new Size(ClientSize.Width, buttonsTop + Theme.ButtonHeight + Theme.S(16));
    }
}
