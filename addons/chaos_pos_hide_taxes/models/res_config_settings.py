# -*- coding: utf-8 -*-

from odoo import fields, models


class ResConfigSettings(models.TransientModel):
    _inherit = 'res.config.settings'

    pos_hide_receipt_taxes = fields.Boolean(
        related='pos_config_id.hide_receipt_taxes',
        readonly=False,
        string='Hide Taxes on Receipt',
    )
