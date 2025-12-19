# -*- coding: utf-8 -*-

from odoo import api, fields, models


class PosConfig(models.Model):
    _inherit = 'pos.config'

    hide_receipt_taxes = fields.Boolean(
        string='Hide Taxes on Receipt',
        default=False,
        help='Hide untaxed amount and tax breakdown from POS receipts. '
             'When enabled, receipts will only show the final total amount without tax details.',
    )

    def _load_pos_data(self, data):
        """Override to ensure hide_receipt_taxes is loaded into POS session."""
        result = super()._load_pos_data(data)

        # Ensure hide_receipt_taxes is in the fields list
        if 'hide_receipt_taxes' not in result['fields']:
            result['fields'].append('hide_receipt_taxes')

        # Ensure the field value is in the data
        for config_data in result['data']:
            if 'hide_receipt_taxes' not in config_data:
                config_data['hide_receipt_taxes'] = self.browse(config_data['id']).hide_receipt_taxes

        return result
