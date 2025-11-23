# -*- coding: utf-8 -*-

from odoo import api, fields, models, _
from odoo.exceptions import ValidationError


class ProductSubtaskTemplate(models.Model):
    _name = 'product.subtask.template'
    _description = 'Product Subtask Template'
    _order = 'product_tmpl_id, sequence, id'

    name = fields.Char(
        string='Subtask Name',
        required=True,
        translate=True,
        help="Name of the subtask that will be created"
    )

    product_tmpl_id = fields.Many2one(
        'product.template',
        string='Product Template',
        required=True,
        ondelete='cascade',
        index=True,
        help="Product to which this subtask template belongs"
    )

    sequence = fields.Integer(
        string='Sequence',
        default=10,
        help="Determine the display order of subtasks"
    )

    allocated_hours = fields.Float(
        string='Allocated Hours',
        default=0.0,
        help="Hours allocated for this subtask"
    )

    description = fields.Html(
        string='Description',
        translate=True,
        help="Detailed description for the subtask"
    )

    active = fields.Boolean(
        string='Active',
        default=True,
        help="If unchecked, this subtask template will not be used"
    )

    company_id = fields.Many2one(
        'res.company',
        string='Company',
        related='product_tmpl_id.company_id',
        store=True,
        readonly=True
    )

    @api.constrains('allocated_hours')
    def _check_allocated_hours(self):
        """Ensure allocated hours is not negative"""
        for template in self:
            if template.allocated_hours < 0:
                raise ValidationError(_('Allocated hours cannot be negative.'))

    def name_get(self):
        """Custom name display: [Product] Subtask Name"""
        result = []
        for template in self:
            if template.product_tmpl_id:
                name = f"[{template.product_tmpl_id.name}] {template.name}"
            else:
                name = template.name
            result.append((template.id, name))
        return result
