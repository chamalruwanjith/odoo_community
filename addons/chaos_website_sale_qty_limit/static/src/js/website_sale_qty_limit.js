/** @odoo-module **/

import publicWidget from "@web/legacy/js/public/public_widget";
import { WebsiteSale } from "@website_sale/js/website_sale";

// Extend WebsiteSale to add quantity limit for upsell products
publicWidget.registry.WebsiteSale.include({

    /**
     * Override to add quantity limit for upsell products
     */
    _changeCartQuantity: function ($input, value, $dom_optional, line_id, productIDs) {
        const $container = $input.closest('[name="website_sale_cart_line_quantity"]');
        const isUpsell = $container.data('is-upsell');
        const maxQty = $container.data('max-qty');

        // If this is an upsell product and value exceeds max, limit it
        if (isUpsell && maxQty > 0 && value > maxQty) {
            value = maxQty;
            $input.val(value);

            // Show notification
            this.displayNotification({
                type: 'warning',
                title: this.env._t("Quantity Limit"),
                message: this.env._t("Maximum quantity for this product is " + maxQty),
            });
        }

        return this._super($input, value, $dom_optional, line_id, productIDs);
    },

    /**
     * Override quantity change to prevent manual input above limit
     */
    _onChangeCartQuantity: function (ev) {
        const $input = $(ev.currentTarget);
        const $container = $input.closest('[name="website_sale_cart_line_quantity"]');
        const isUpsell = $container.data('is-upsell');
        const maxQty = $container.data('max-qty');

        if (isUpsell && maxQty > 0) {
            let value = parseInt($input.val() || 0, 10);
            if (value > maxQty) {
                $input.val(maxQty);
                ev.preventDefault();

                this.displayNotification({
                    type: 'warning',
                    title: this.env._t("Quantity Limit"),
                    message: this.env._t("Maximum quantity for this product is " + maxQty),
                });

                // Trigger change with corrected value
                setTimeout(() => {
                    $input.trigger('change');
                }, 100);
                return;
            }
        }

        return this._super(ev);
    },

    /**
     * Update plus button state after quantity changes
     */
    start: function () {
        this._super.apply(this, arguments).then(() => {
            this._updatePlusButtonStates();
        });
    },

    /**
     * Disable plus button when upsell product reaches max quantity
     */
    _updatePlusButtonStates: function () {
        $('[name="website_sale_cart_line_quantity"]').each(function () {
            const $container = $(this);
            const isUpsell = $container.data('is-upsell');
            const maxQty = $container.data('max-qty');

            if (isUpsell && maxQty > 0) {
                const $input = $container.find('.js_quantity');
                const currentQty = parseInt($input.val() || 0, 10);
                const $plusBtn = $container.find('.js_add_cart_json').last();

                if (currentQty >= maxQty) {
                    $plusBtn.prop('disabled', true).addClass('opacity-50 pe-none');
                } else {
                    $plusBtn.prop('disabled', false).removeClass('opacity-50 pe-none');
                }
            }
        });
    },
});

// Update button states when DOM is ready
$(document).ready(function () {
    // Update states on page load
    setTimeout(() => {
        $('[name="website_sale_cart_line_quantity"]').each(function () {
            const $container = $(this);
            const isUpsell = $container.data('is-upsell');
            const maxQty = $container.data('max-qty');

            if (isUpsell && maxQty > 0) {
                const $input = $container.find('.js_quantity');
                const currentQty = parseInt($input.val() || 0, 10);
                const $plusBtn = $container.find('a.js_add_cart_json').last();

                if (currentQty >= maxQty) {
                    $plusBtn.prop('disabled', true).addClass('opacity-50 pe-none');
                    $plusBtn.css('cursor', 'not-allowed');
                }
            }
        });
    }, 500);
});
