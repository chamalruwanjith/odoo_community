# -*- coding: utf-8 -*-

from odoo import fields, models


class PosConfig(models.Model):
    _inherit = 'pos.config'

    hide_receipt_taxes = fields.Boolean(
        string='Hide Taxes on Receipt',
        default=False,
        help='Hide untaxed amount and tax breakdown from POS receipts. '
             'When enabled, receipts will only show the final total amount without tax details.',
    )
