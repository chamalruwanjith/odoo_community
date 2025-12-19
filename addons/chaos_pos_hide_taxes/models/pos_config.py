# -*- coding: utf-8 -*-

from odoo import api, fields, models


class PosConfig(models.Model):
    _inherit = 'pos.config'

    hide_receipt_taxes = fields.Boolean(
        string='Hide Taxes on Receipt',
        default=False,
        help='Hide untaxed amount and tax breakdown from POS receipts. '
             'When enabled, receipts will only show the final total amount without tax details.',
        company_dependent=True,
    )

    @api.model
    def _load_pos_data_fields(self, config_id):
        """Add hide_receipt_taxes to the fields loaded in the POS session."""
        fields = super()._load_pos_data_fields(config_id)
        fields.append('hide_receipt_taxes')
        return fields
