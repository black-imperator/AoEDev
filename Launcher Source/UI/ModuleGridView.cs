using System;
using System.Drawing;
using System.Windows.Forms;

namespace AoELauncher.UI;

/// <summary>
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
/// </summary>
public class ModuleGridView : DataGridView
{
    private Point _dragStart = Point.Empty;
    private bool _dragArmed;
    private bool _deferredSingleSelectPending;
    private int _deferredRowIndex = -1;

    /// <summary>Raised once the mouse has moved far enough (from a valid row, held button) to start a drag-drop gesture.</summary>
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

    public ModuleGridView()
    {
        ShowCellToolTips = false;
    }

    protected override void Dispose(bool disposing)
    {
        if (disposing) _cellToolTip.Dispose();
        base.Dispose(disposing);
    }

    /// <summary>Shows, changes or hides the tooltip to match whatever cell is under the cursor right now.</summary>
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
            _cellToolTip.Show(text, this, pt.X + 16, pt.Y + 20, ToolTipDurationMs);
    }

    private void ResetCellToolTip()
    {
        _tipRow = _tipColumn = -1;
        _tipText = "";
        if (IsHandleCreated) _cellToolTip.Hide(this);
    }

    /// <summary>Rows being rebuilt (Refresh, drag-drop) can change what's under a stationary cursor; re-check once the batch is done.</summary>
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
        UpdateCellToolTip();
    }

    protected override void OnScroll(ScrollEventArgs e)
    {
        base.OnScroll(e);
        UpdateCellToolTip();
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
