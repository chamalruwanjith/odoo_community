/** @odoo-module **/
/**
 * ChaosHub Theme Toggle
 * Dark/Light theme switcher with localStorage persistence
 */

import publicWidget from "@web/legacy/js/public/public_widget";

publicWidget.registry.ThemeToggle = publicWidget.Widget.extend({
    selector: 'body',

    events: {
        'click .theme-toggle-btn': '_onToggleTheme',
    },

    /**
     * Initialize theme on page load
     */
    start() {
        this._super(...arguments);
        this._initTheme();
        this._createToggleButton();
    },

    /**
     * Initialize theme based on localStorage or system preference
     */
    _initTheme() {
        const savedTheme = localStorage.getItem('chaoshub-theme');
        const prefersDark = window.matchMedia('(prefers-color-scheme: dark)').matches;

        if (savedTheme === 'dark' || (!savedTheme && prefersDark)) {
            this._enableDarkTheme();
        } else {
            this._enableLightTheme();
        }

        // Listen for system theme changes
        window.matchMedia('(prefers-color-scheme: dark)').addEventListener('change', (e) => {
            if (!localStorage.getItem('chaoshub-theme')) {
                if (e.matches) {
                    this._enableDarkTheme();
                } else {
                    this._enableLightTheme();
                }
            }
        });
    },

    /**
     * Create floating theme toggle button
     */
    _createToggleButton() {
        // Check if button already exists
        if (document.querySelector('.theme-toggle-btn')) {
            return;
        }

        const button = document.createElement('button');
        button.className = 'theme-toggle-btn';
        button.setAttribute('aria-label', 'Toggle dark mode');
        button.setAttribute('title', 'Toggle dark/light theme');

        const isDark = document.body.classList.contains('dark-theme');
        button.innerHTML = isDark
            ? '<i class="fa fa-sun-o icon-sun"></i>'
            : '<i class="fa fa-moon-o icon-moon"></i>';

        document.body.appendChild(button);
    },

    /**
     * Handle theme toggle button click
     */
    _onToggleTheme(ev) {
        ev.preventDefault();
        const isDark = document.body.classList.contains('dark-theme');

        if (isDark) {
            this._enableLightTheme();
            localStorage.setItem('chaoshub-theme', 'light');
        } else {
            this._enableDarkTheme();
            localStorage.setItem('chaoshub-theme', 'dark');
        }

        this._updateToggleButton();
    },

    /**
     * Enable dark theme
     */
    _enableDarkTheme() {
        document.body.classList.add('dark-theme');
        document.documentElement.setAttribute('data-theme', 'dark');
    },

    /**
     * Enable light theme
     */
    _enableLightTheme() {
        document.body.classList.remove('dark-theme');
        document.documentElement.setAttribute('data-theme', 'light');
    },

    /**
     * Update toggle button icon
     */
    _updateToggleButton() {
        const button = document.querySelector('.theme-toggle-btn');
        if (!button) return;

        const isDark = document.body.classList.contains('dark-theme');
        button.innerHTML = isDark
            ? '<i class="fa fa-sun-o icon-sun"></i>'
            : '<i class="fa fa-moon-o icon-moon"></i>';

        button.setAttribute('title', isDark ? 'Switch to light theme' : 'Switch to dark theme');
    },
});

export default publicWidget.registry.ThemeToggle;
