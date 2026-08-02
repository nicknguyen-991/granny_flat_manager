/**
 * Django Admin changelist: clicking anywhere on a result row
 * opens the change form (same URL as the first-column link).
 * Checkbox / button clicks are ignored.
 */
(function () {
    'use strict';

    function initRowLinks() {
        const table = document.getElementById('result_list');
        if (!table) {
            return;
        }

        table.querySelectorAll('tbody tr').forEach(function (row) {
            row.addEventListener('click', function (event) {
                // Don't navigate when interacting with form controls.
                if (
                    event.target.closest(
                        'input, button, select, textarea, label, .action-select'
                    )
                ) {
                    return;
                }

                // If user clicked a real link, let the browser handle it.
                if (event.target.closest('a')) {
                    return;
                }

                const link = row.querySelector('th a[href], td a[href]');
                if (link && link.getAttribute('href')) {
                    window.location.href = link.href;
                }
            });
        });
    }

    if (document.readyState === 'loading') {
        document.addEventListener('DOMContentLoaded', initRowLinks);
    } else {
        initRowLinks();
    }
})();
