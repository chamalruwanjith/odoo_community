# -*- coding: utf-8 -*-
from odoo import models, fields, api

class PurchaseOrder(models.Model):
    _inherit = 'purchase.order'

    loading_plan_ids = fields.One2many('loading.plan', 'purchase_order_id', string='Loading Plans')
    loading_plan_count = fields.Integer(string='Loading Plan Count', compute='_compute_loading_plan_count')
    
    @api.depends('loading_plan_ids')
    def _compute_loading_plan_count(self):
        for order in self:
            order.loading_plan_count = len(order.loading_plan_ids)
    
    def action_view_loading_plans(self):
        self.ensure_one()
        return {
            'name': 'Loading Plans',
            'type': 'ir.actions.act_window',
            'res_model': 'loading.plan',
            'view_mode': 'list,form',
            'domain': [('purchase_order_id', '=', self.id)],
            'context': {'default_purchase_order_id': self.id}
        }
    
    def action_create_loading_plan(self):
        self.ensure_one()
        return {
            'name': 'Create Loading Plan',
            'type': 'ir.actions.act_window',
            'res_model': 'loading.plan',
            'view_mode': 'form',
            'context': {'default_purchase_order_id': self.id},
            'target': 'new',
        }
