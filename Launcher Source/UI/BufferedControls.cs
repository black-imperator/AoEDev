using System.Windows.Forms;

namespace AoELauncher.UI;

// Standard WinForms controls repaint without double buffering, which shows up as flicker and
// stutter while the window is being resized (every child is invalidated and redrawn directly to
// the screen). DoubleBuffered is a protected property, so each control type needs a tiny subclass
// to turn it on.

public class BufferedPanel : Panel
{
    public BufferedPanel() { DoubleBuffered = true; }
}

public class BufferedGroupBox : GroupBox
{
    public BufferedGroupBox() { DoubleBuffered = true; }
}

public class BufferedSplitContainer : SplitContainer
{
    public BufferedSplitContainer() { DoubleBuffered = true; }
}
