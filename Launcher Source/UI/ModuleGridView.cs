using System;
using System.Drawing;
using System.Windows.Forms;

namespace AoELauncher.UI;

/// A plain DataGridView with MultiSelect=true already supports Ctrl-click
/// (toggle) and Shift-click (range) natively and correctly -- the previous
/// version of this app tried to reimplement that logic in a MouseDown event
/// handler and made it worse, because DataGridView's own default selection
/// handling runs as part of its internal OnMouseDown processing, which
/// completes *before* a subscribed public MouseDown event handler ever
/// runs. That ordering is also why "click a row, then drag the whole
/// multi-selection" doesn't work with a plain DataGridView: by the time any
/// event handler gets a chance to intervene, the grid has already collapsed
/// the selection down to just the clicked row.
///
/// The fix is to override the protected OnMouseDown method itself (which
/// runs *before* any of that), and selectively skip calling the base
/// implementation for exactly one case: a plain (no Ctrl/Shift) click on a
/// row that's already part of an existing multi-row selection. In that one
/// case, the selection is left completely untouched (so a drag beginning
/// here still carries the full group), and is only collapsed down to the
/// single clicked row afterward, in OnMouseUp, if no drag actually
/// happened. Every other case (Ctrl-click, Shift-click, clicking an
/// unselected row) falls straight through to the grid's own correct,
/// well-tested default behavior.
public class ModuleGridView : DataGridView
{
    private Point _dragStart = Point.Empty;
    private bool _dragArmed;
    private bool _deferredSingleSelectPending;
    private int _deferredRowIndex = -1;

    // --- Module|Author divider ---------------------------------------------------------------
    // The grid's built-in column resizing only applies the new width when the mouse is released
    // (and treats a divider as belonging to the column on its left), so the one adjustable divider
    // -- between the Name and Author columns -- is handled here instead: the header is hit-tested
    // near that boundary, and while the button is held the desired Name width is reported on every
    // mouse move so the owner can update the layout live.

    private bool _dividerDragging;
    private int _dividerDragStartX;
    private int _dividerDragStartWidth;

    /// Raised on every mouse move while the divider is dragged, with the Name column width the
    /// drag is asking for (the owner decides what that means and may clamp it).
    public event EventHandler<int>? DividerDragged;

    /// Raised once when the divider drag ends.
    public event EventHandler? DividerDragEnded;

    private bool IsOnDivider(int x, int y)
    {
        if (y < 0 || y >= ColumnHeadersHeight || Columns.Count == 0) return false;
        var name = Columns["Name"];
        if (name == null || !name.Visible) return false;
        var right = GetColumnDisplayRectangle(name.Index, false).Right;
        return Math.Abs(x - right) <= Theme.S(4);
    }

    /// Raised once the mouse has moved far enough (from a valid row, held button) to start a drag-drop gesture.
    public event EventHandler? DragThresholdReached;

    // --- Cell tooltips -----------------------------------------------------------------------
    // DataGridView's built-in cell tooltips (ShowCellToolTips) use a private internal ToolTip that
    // hides/re-shows itself on every cell change and can't be tuned without reflection, which
    // previously led to tooltips showing the neighboring row's text. Instead, the built-in ones are
    // turned off and this grid owns a normal ToolTip, re-deriving the text from a live hit-test of
    // the cursor each time it could have changed (mouse move, wheel, leave, rows rebuilt), so it
    // always reflects the row that is actually under the mouse. Text comes from each cell's
    // ToolTipText, which is still how callers supply it.

    private readonly ToolTip _cellToolTip = new()
    {
        InitialDelay = 0,
        ReshowDelay = 0,
        UseFading = false,
        UseAnimation = false,
    };

    private const int ToolTipDurationMs = 30000;
    private int _tipRow = -1;
    private int _tipColumn = -1;
    private string _tipText = "";
    private bool _tipRefreshQueued;

    // While the grid is scrolling, the tooltip is hidden and not re-derived on every scroll tick;
    // it comes back once scrolling has been quiet for a moment. Showing/hiding a tooltip window
    // over the grid in the middle of a scroll (the grid blits its old pixels up/down and only
    // repaints the newly exposed strip) is the likeliest cause of rows briefly appearing
    // duplicated until scrolling stops.
    private readonly System.Windows.Forms.Timer _scrollSettleTimer = new() { Interval = 150 };

    public ModuleGridView()
    {
        ShowCellToolTips = false;
        Theme.StyleToolTip(_cellToolTip, Theme.S(420), () => _tipText);

        // DataGridView doesn't double-buffer by default; without it, resizing the window repaints
        // every visible cell straight to the screen and stutters badly.
        DoubleBuffered = true;

        _scrollSettleTimer.Tick += (s, e) =>
        {
            _scrollSettleTimer.Stop();
            UpdateCellToolTip();
        };
    }

    /// Hides the tooltip and defers bringing it back until scrolling has settled.
    private void OnScrolling()
    {
        ResetCellToolTip();
        _scrollSettleTimer.Stop();
        _scrollSettleTimer.Start();

        // Repaint the whole viewport rather than trusting the partial blit-and-patch a scroll
        // normally does, so no stale rows can be left behind mid-scroll.
        Invalidate();
    }

    protected override void Dispose(bool disposing)
    {
        if (disposing) { _scrollSettleTimer.Dispose(); _cellToolTip.Dispose(); }
        base.Dispose(disposing);
    }

    /// Shows, changes or hides the tooltip to match whatever cell is under the cursor right now.
    private void UpdateCellToolTip()
    {
        if (!IsHandleCreated || IsDisposed) return;

        var pt = PointToClient(Cursor.Position);
        int row = -1, column = -1;
        var text = "";

        if (ClientRectangle.Contains(pt))
        {
            var hit = HitTest(pt.X, pt.Y);
            if (hit.Type == DataGridViewHitTestType.Cell &&
                hit.RowIndex >= 0 && hit.RowIndex < Rows.Count &&
                hit.ColumnIndex >= 0 && hit.ColumnIndex < Columns.Count)
            {
                row = hit.RowIndex;
                column = hit.ColumnIndex;
                text = Rows[row].Cells[column].ToolTipText ?? "";
            }
        }

        if (row == _tipRow && column == _tipColumn && text == _tipText) return;

        _tipRow = row;
        _tipColumn = column;
        _tipText = text;

        if (text.Length == 0)
            _cellToolTip.Hide(this);
        else
            _cellToolTip.Show(text, this, pt.X + Theme.S(16), pt.Y + Theme.S(20), ToolTipDurationMs);
    }

    private void ResetCellToolTip()
    {
        _tipRow = _tipColumn = -1;
        _tipText = "";
        if (IsHandleCreated) _cellToolTip.Hide(this);
    }

    /// Rows being rebuilt (Refresh, drag-drop) can change what's under a stationary cursor; re-check once the batch is done.
    private void QueueCellToolTipRefresh()
    {
        if (_tipRefreshQueued || !IsHandleCreated) return;
        _tipRefreshQueued = true;
        BeginInvoke(new Action(() =>
        {
            _tipRefreshQueued = false;
            UpdateCellToolTip();
        }));
    }

    protected override void OnRowsAdded(DataGridViewRowsAddedEventArgs e)
    {
        base.OnRowsAdded(e);
        QueueCellToolTipRefresh();
    }

    protected override void OnRowsRemoved(DataGridViewRowsRemovedEventArgs e)
    {
        base.OnRowsRemoved(e);
        QueueCellToolTipRefresh();
    }

    protected override void OnMouseWheel(MouseEventArgs e)
    {
        base.OnMouseWheel(e);
        OnScrolling();
    }

    protected override void OnScroll(ScrollEventArgs e)
    {
        base.OnScroll(e);
        OnScrolling();
    }

    protected override void OnMouseLeave(EventArgs e)
    {
        base.OnMouseLeave(e);
        ResetCellToolTip();
    }

    protected override void OnMouseDown(MouseEventArgs e)
    {
        _deferredSingleSelectPending = false;
        _deferredRowIndex = -1;
        _dragArmed = false;

        if (IsHandleCreated) _cellToolTip.Hide(this); // hidden on click; returns when the cursor enters another cell

        if (e.Button == MouseButtons.Left && IsOnDivider(e.X, e.Y))
        {
            _dividerDragging = true;
            _dividerDragStartX = e.X;
            _dividerDragStartWidth = Columns["Name"]!.Width;
            Capture = true;
            return; // not a header click (sort) or selection change
        }

        var hit = HitTest(e.X, e.Y);
        var infoCol = Columns["Info"];
        bool onInfoButton = infoCol != null && hit.ColumnIndex == infoCol.Index;

        if (e.Button == MouseButtons.Left && hit.RowIndex >= 0 && !onInfoButton)
        {
            _dragArmed = true;
            _dragStart = e.Location;

            bool ctrl = (ModifierKeys & Keys.Control) == Keys.Control;
            bool shift = (ModifierKeys & Keys.Shift) == Keys.Shift;

            if (!ctrl && !shift && hit.RowIndex < Rows.Count &&
                Rows[hit.RowIndex].Selected && SelectedRows.Count > 1)
            {
                _deferredSingleSelectPending = true;
                _deferredRowIndex = hit.RowIndex;
                return; // deliberately skip base.OnMouseDown -- don't let the grid collapse the selection yet
            }
        }

        base.OnMouseDown(e);
    }

    protected override void OnMouseMove(MouseEventArgs e)
    {
        if (_dividerDragging)
        {
            DividerDragged?.Invoke(this, _dividerDragStartWidth + e.X - _dividerDragStartX);
            return;
        }

        var wantCursor = e.Button == MouseButtons.None && IsOnDivider(e.X, e.Y) ? Cursors.VSplit : Cursors.Default;
        if (Cursor != wantCursor) Cursor = wantCursor;

        if (_dragArmed && e.Button == MouseButtons.Left)
        {
            if (Math.Abs(e.X - _dragStart.X) >= SystemInformation.DragSize.Width ||
                Math.Abs(e.Y - _dragStart.Y) >= SystemInformation.DragSize.Height)
            {
                _dragArmed = false;
                _deferredSingleSelectPending = false; // a drag is happening -- keep the (already-correct) selection intact
                DragThresholdReached?.Invoke(this, EventArgs.Empty);
            }
        }
        base.OnMouseMove(e);
        if (e.Button == MouseButtons.None) UpdateCellToolTip();
    }

    protected override void OnMouseUp(MouseEventArgs e)
    {
        if (_dividerDragging)
        {
            _dividerDragging = false;
            Capture = false;
            DividerDragEnded?.Invoke(this, EventArgs.Empty);
            return;
        }

        if (_dragArmed && _deferredSingleSelectPending &&
            _deferredRowIndex >= 0 && _deferredRowIndex < Rows.Count)
        {
            // No drag happened after all -- this was just a click, so now collapse to just this row.
            ClearSelection();
            Rows[_deferredRowIndex].Selected = true;
        }

        _dragArmed = false;
        _deferredSingleSelectPending = false;
        _deferredRowIndex = -1;
        base.OnMouseUp(e);
    }
}
