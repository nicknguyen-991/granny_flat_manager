/**
 * Django Admin changelist: Excel-style column autofit.
 * Double-click the border between two column headers to fit that column to content.
 * Drag the same border to resize manually.
 */
(function () {
    'use strict';

    function measureTextWidth(text, sampleEl) {
        const canvas = measureTextWidth._canvas || document.createElement('canvas');
        measureTextWidth._canvas = canvas;
        const ctx = canvas.getContext('2d');
        const style = window.getComputedStyle(sampleEl);
        ctx.font = [
            style.fontStyle,
            style.fontVariant,
            style.fontWeight,
            style.fontSize,
            style.fontFamily,
        ].join(' ');
        return ctx.measureText(text || '').width;
    }

    function autofitColumn(table, colIndex) {
        const headerCell = table.querySelectorAll('thead th')[colIndex];
        if (!headerCell) {
            return;
        }

        let maxWidth = measureTextWidth(headerCell.innerText.trim(), headerCell) + 36;

        table.querySelectorAll('tbody tr').forEach(function (row) {
            const cell = row.children[colIndex];
            if (!cell) {
                return;
            }
            const width = measureTextWidth(cell.innerText.trim(), cell) + 28;
            if (width > maxWidth) {
                maxWidth = width;
            }
        });

        // Keep a sensible min/max so one long cell does not blow up the layout.
        maxWidth = Math.max(72, Math.min(maxWidth, 480));

        const colgroup = ensureColgroup(table);
        const col = colgroup.children[colIndex];
        if (col) {
            col.style.width = maxWidth + 'px';
        }
        headerCell.style.width = maxWidth + 'px';
    }

    function ensureColgroup(table) {
        let colgroup = table.querySelector('colgroup');
        const headerCells = table.querySelectorAll('thead th');
        if (!colgroup) {
            colgroup = document.createElement('colgroup');
            headerCells.forEach(function () {
                colgroup.appendChild(document.createElement('col'));
            });
            table.insertBefore(colgroup, table.firstChild);
        } else if (colgroup.children.length < headerCells.length) {
            while (colgroup.children.length < headerCells.length) {
                colgroup.appendChild(document.createElement('col'));
            }
        }
        return colgroup;
    }

    function enableColumnResize(table) {
        ensureColgroup(table);
        const headers = table.querySelectorAll('thead th');

        headers.forEach(function (th, index) {
            // Skip action checkbox column edge cases; still allow autofit.
            if (th.querySelector('.col-resize-handle')) {
                return;
            }

            const handle = document.createElement('span');
            handle.className = 'col-resize-handle';
            handle.title = 'Double-click to autofit column';
            th.appendChild(handle);

            handle.addEventListener('dblclick', function (event) {
                event.preventDefault();
                event.stopPropagation();
                autofitColumn(table, index);
            });

            handle.addEventListener('mousedown', function (event) {
                if (event.detail > 1) {
                    // Let dblclick handle autofit; ignore drag start on second click.
                    return;
                }
                event.preventDefault();
                event.stopPropagation();

                handle.classList.add('is-active');
                const startX = event.pageX;
                const startWidth = th.offsetWidth;
                const colgroup = ensureColgroup(table);
                const col = colgroup.children[index];

                function onMouseMove(moveEvent) {
                    const newWidth = Math.max(60, startWidth + (moveEvent.pageX - startX));
                    th.style.width = newWidth + 'px';
                    if (col) {
                        col.style.width = newWidth + 'px';
                    }
                }

                function onMouseUp() {
                    handle.classList.remove('is-active');
                    document.removeEventListener('mousemove', onMouseMove);
                    document.removeEventListener('mouseup', onMouseUp);
                }

                document.addEventListener('mousemove', onMouseMove);
                document.addEventListener('mouseup', onMouseUp);
            });
        });
    }

    function init() {
        const table = document.getElementById('result_list');
        if (table) {
            enableColumnResize(table);
        }
    }

    if (document.readyState === 'loading') {
        document.addEventListener('DOMContentLoaded', init);
    } else {
        init();
    }
})();
