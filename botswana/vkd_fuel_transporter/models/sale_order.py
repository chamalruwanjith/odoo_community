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
