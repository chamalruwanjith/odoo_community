# -*- coding: utf-8 -*-
from odoo import models, fields, api


class SaleOrder(models.Model):
    _inherit = 'sale.order'


    transporter_id = fields.Many2one('res.partner', string='Transporter', domain=[('is_transporter', '=', True)], tracking=True)
    transporter_vehicle_id = fields.Many2one('fleet.vehicle', string='Vehicle (Reg Number)', domain="[('transporter_id', '=', transporter_id)]", tracking=True)

    trailer_1_id = fields.Many2one('fleet.trailer', string='Trailer 1', tracking=True)
    trailer_2_id = fields.Many2one('fleet.trailer', string='Trailer 2', tracking=True)
    trailer_3_id = fields.Many2one('fleet.trailer', string='Trailer 3', tracking=True)

    location_rate = fields.Float(string='Location Rate', digits=(16, 2), tracking=True, compute='_compute_location_rate', inverse='_inverse_location_rate', store=True)

    @api.depends('partner_id')
    def _compute_location_rate(self):
        for order in self:
            order.location_rate = order.partner_id.product_id.list_price

    def _inverse_location_rate(self):
        for order in self:
            order.location_rate = order.location_rate

    @api.onchange('transporter_id')
    def _onchange_transporter_id(self):
        if not self.transporter_id:
            self.transporter_vehicle_id = False
            self.trailer_1_id = False
            self.trailer_2_id = False
            self.trailer_3_id = False
        else:
            if self.transporter_vehicle_id and self.transporter_vehicle_id.transporter_id != self.transporter_id:
                self.transporter_vehicle_id = False

    @api.onchange('transporter_vehicle_id')
    def _onchange_transporter_vehicle_id(self):
        if self.transporter_vehicle_id:
            self.trailer_1_id = self.transporter_vehicle_id.trailer_1_id
            self.trailer_2_id = self.transporter_vehicle_id.trailer_2_id
            self.trailer_3_id = self.transporter_vehicle_id.trailer_3_id
        else:
            self.trailer_1_id = False
            self.trailer_2_id = False
            self.trailer_3_id = False

    def _action_confirm(self):
        """Override to pass transporter details through context for picking creation"""
        # Add transporter details to context so pickings can read them during creation
        ctx = dict(self.env.context or {})
        for order in self:
            if order.transporter_id:
                ctx.update({
                    'default_transporter_id': order.transporter_id.id,
                    'default_transporter_vehicle_id': order.transporter_vehicle_id.id if order.transporter_vehicle_id else False,
                    'default_trailer_1_id': order.trailer_1_id.id if order.trailer_1_id else False,
                    'default_trailer_2_id': order.trailer_2_id.id if order.trailer_2_id else False,
                    'default_trailer_3_id': order.trailer_3_id.id if order.trailer_3_id else False,
                })
                break  # Use first order's transporter if multiple orders

        # Call super with updated context
        res = super(SaleOrder, self.with_context(ctx))._action_confirm()
        return res

    def copy_transporter_from_purchase(self, purchase_order):
        """Helper method to copy transporter details from PO to SO (used by dropship module)"""
        self.ensure_one()
        if purchase_order:
            self.write({
                'transporter_id': purchase_order.transporter_id.id if purchase_order.transporter_id else False,
                'transporter_vehicle_id': purchase_order.transporter_vehicle_id.id if purchase_order.transporter_vehicle_id else False,
                'trailer_1_id': purchase_order.trailer_1_id.id if purchase_order.trailer_1_id else False,
                'trailer_2_id': purchase_order.trailer_2_id.id if purchase_order.trailer_2_id else False,
                'trailer_3_id': purchase_order.trailer_3_id.id if purchase_order.trailer_3_id else False,
            })
