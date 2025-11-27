# -*- coding: utf-8 -*-
from odoo import models, fields

class ProductTemplate(models.Model):
    _inherit = 'product.template'

    product_identifier = fields.Selection([
        ('diesel', 'Diesel'),
        ('petrol', 'Petrol')
    ], string='Product Identifier')
