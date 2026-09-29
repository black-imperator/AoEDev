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
        Width = 580;
        Height = 430;
        StartPosition = FormStartPosition.CenterParent;
        FormBorderStyle = FormBorderStyle.FixedDialog;
        MaximizeBox = false;
        MinimizeBox = false;
        Theme.StyleForm(this);

        var box = new ReadOnlySelectableTextBox
        {
            Left = 12, Top = 12, Width = 540, Height = 280,
            ScrollBars = ScrollBars.Vertical,
            Text = message,
        };
        Theme.StyleTextBox(box);
        Controls.Add(box);

        var buttonsTop = box.Bottom + 16;
        var btnRecheck = new FlatButton { Text = "Re-check", Left = 12, Top = buttonsTop, Width = 140, Height = Theme.ButtonHeight };
        var btnContinue = new FlatButton { Text = "Continue Anyway", Left = 160, Top = buttonsTop, Width = 160, Height = Theme.ButtonHeight };
        var btnQuit = new FlatButton { Text = "Quit", Left = 428, Top = buttonsTop, Width = 124, Height = Theme.ButtonHeight };
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

        Height = buttonsTop + Theme.ButtonHeight + 60; // guarantee enough room below the buttons, regardless of DPI/title-bar quirks
    }
}
