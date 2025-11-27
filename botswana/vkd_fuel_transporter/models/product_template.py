from odoo import _, api, fields, models


class ProductTemplate(models.Model):
    _inherit = "product.template"

    is_location_rate = fields.Boolean(
        'Is Location Rate?',
        help='Transporter location rate to the customer master')

    is_transporter_claimed = fields.Boolean(string='Is Transporter Claimed?')
