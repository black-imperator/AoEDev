using System.Windows.Forms;

namespace AoELauncher.UI;

/// <summary>
/// A plain WinForms Button shows a dotted focus-cue rectangle once it's been
/// clicked, and that rectangle stays visible until some other control takes
/// focus -- which reads as an extra "bolded" border that doesn't go away.
/// Overriding ShowFocusCues is the standard, documented way to suppress
/// just that visual cue without otherwise changing button behavior.
/// </summary>
public class FlatButton : Button
{
    protected override bool ShowFocusCues => false;
}
