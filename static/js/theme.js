/**
 * Persist light/dark theme for Granny Flat Manager pages.
 */
(function () {
    'use strict';

    var STORAGE_KEY = 'gfm-theme';

    function currentTheme() {
        return document.documentElement.getAttribute('data-theme') === 'dark' ? 'dark' : 'light';
    }

    function applyTheme(theme) {
        document.documentElement.setAttribute('data-theme', theme);
        try {
            localStorage.setItem(STORAGE_KEY, theme);
        } catch (err) {
            /* ignore quota / private mode */
        }
        var button = document.getElementById('theme-toggle');
        if (button) {
            button.setAttribute(
                'aria-label',
                theme === 'dark' ? 'Switch to light mode' : 'Switch to dark mode'
            );
            button.setAttribute('title', theme === 'dark' ? 'Light mode' : 'Dark mode');
        }
    }

    document.addEventListener('DOMContentLoaded', function () {
        applyTheme(currentTheme());
        var button = document.getElementById('theme-toggle');
        if (!button) {
            return;
        }
        button.addEventListener('click', function () {
            applyTheme(currentTheme() === 'dark' ? 'light' : 'dark');
        });
    });
})();
