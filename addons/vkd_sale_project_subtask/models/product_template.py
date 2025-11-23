# -*- coding: utf-8 -*-

from odoo import api, fields, models, _


class ProductTemplate(models.Model):
    _inherit = 'product.template'

    subtask_template_ids = fields.One2many(
        'product.subtask.template',
        'product_tmpl_id',
        string='Subtask Templates',
        help="Define subtasks that will be automatically created when a task is generated from a sale order"
    )

    subtask_template_count = fields.Integer(
        string='Subtask Templates Count',
        compute='_compute_subtask_template_count',
        store=True
    )

    @api.depends('subtask_template_ids')
    def _compute_subtask_template_count(self):
        """Count active subtask templates"""
        for product in self:
            product.subtask_template_count = len(product.subtask_template_ids.filtered('active'))
