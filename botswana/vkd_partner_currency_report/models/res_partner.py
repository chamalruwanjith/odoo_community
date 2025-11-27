# -*- coding: utf-8 -*-

from odoo import models, fields, api


class ResPartner(models.Model):
    _inherit = 'res.partner'

    partner_currency_id = fields.Many2one(
        'res.currency',
        string='Partner Currency',
        help='Default currency for transactions with this partner. '
             'This will be used for currency-wise reporting.',
        tracking=True,
    )

    @api.onchange('country_id')
    def _onchange_country_id_set_currency(self):
        """Suggest currency based on partner's country"""
        if self.country_id and self.country_id.currency_id:
            if not self.partner_currency_id:
                self.partner_currency_id = self.country_id.currency_id
