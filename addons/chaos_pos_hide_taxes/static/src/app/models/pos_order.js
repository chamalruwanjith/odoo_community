/** @odoo-module */

import { PosOrder } from "@point_of_sale/app/models/pos_order";
import { patch } from "@web/core/utils/patch";

patch(PosOrder.prototype, {
    /**
     * Override export_for_printing to include hide_receipt_taxes setting
     */
    export_for_printing(baseUrl, headerData) {
        const result = super.export_for_printing(...arguments);

        // Add the hide_receipt_taxes setting from config
        // Debug: log the config value
        console.log('[chaos_pos_hide_taxes] Config value:', this.config.hide_receipt_taxes);
        console.log('[chaos_pos_hide_taxes] Full config:', this.config);

        result.hide_receipt_taxes = Boolean(this.config.hide_receipt_taxes);

        return result;
    },
});
