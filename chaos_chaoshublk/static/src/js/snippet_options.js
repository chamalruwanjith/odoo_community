/** @odoo-module **/
/**
 * ChaosHub Snippet Options for Website Builder
 * Custom options and behaviors for ChaosHub snippets in edit mode
 */

import options from "@web_editor/js/editor/snippets.options";

// Hero snippet options
options.registry.ChaosHubHero = options.Class.extend({
    /**
     * Change hero background style
     */
    selectBackgroundStyle(previewMode, widgetValue, params) {
        this.$target.removeClass('hero-gradient hero-solid hero-image');
        this.$target.addClass(widgetValue);
    },

    /**
     * Change hero height
     */
    selectHeight(previewMode, widgetValue, params) {
        this.$target.removeClass('hero-sm hero-lg');
        if (widgetValue) {
            this.$target.addClass(widgetValue);
        }
    },
});

// Features snippet options
options.registry.ChaosHubFeatures = options.Class.extend({
    /**
     * Change number of columns
     */
    selectColumns(previewMode, widgetValue, params) {
        const $grid = this.$target.find('.grid');
        $grid.removeClass('grid-2 grid-3 grid-4');
        $grid.addClass('grid-' + widgetValue);
    },
});

// CTA snippet options
options.registry.ChaosHubCTA = options.Class.extend({
    /**
     * Toggle full width
     */
    toggleFullWidth(previewMode, widgetValue, params) {
        this.$target.toggleClass('cta-full-width', widgetValue);
    },
});

export default {
    ChaosHubHero: options.registry.ChaosHubHero,
    ChaosHubFeatures: options.registry.ChaosHubFeatures,
    ChaosHubCTA: options.registry.ChaosHubCTA,
};
