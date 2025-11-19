# -*- coding: utf-8 -*-

from odoo import models, fields, api, _


class ResPartner(models.Model):
    _inherit = 'res.partner'

    is_dropship_customer = fields.Boolean(
        string='Is Dropship Customer',
        default=False,
        help='Mark this partner as a placeholder dropship customer. '
             'This customer will be auto-selected when creating SO from PO. '
             'Must be replaced with actual customer before confirming the SO.'
    )
