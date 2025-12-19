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
        result.hide_receipt_taxes = this.config.hide_receipt_taxes || false;

        return result;
    },
});
