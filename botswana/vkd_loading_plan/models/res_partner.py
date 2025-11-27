# -*- coding: utf-8 -*-
from odoo import models, fields


class ResPartner(models.Model):
    _inherit = 'res.partner'

    fuel_supplier_type = fields.Selection([
        ('namcor', 'Namcor'),
        ('puma', 'Puma Energy'),
        ('vivo', 'Vivo'),
        ('sasol', 'Sasol'),
        ('standard', 'Standard Supplier'),
    ], string='Fuel Supplier Type', help='Select the fuel supplier type for loading plan template')
