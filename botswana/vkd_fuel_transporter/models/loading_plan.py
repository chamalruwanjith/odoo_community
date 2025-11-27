# -*- coding: utf-8 -*-
from odoo import models, fields, api


class LoadingPlan(models.Model):
    _inherit = 'loading.plan'

    # Replace existing char fields with proper transporter and vehicle fields
    transporter_id = fields.Many2one('res.partner', string='Transporter', domain=[('is_transporter', '=', True)], tracking=True)
    transporter_vehicle_id = fields.Many2one('fleet.vehicle', string='Vehicle (Reg Number)', domain="[('transporter_id', '=', transporter_id)]", tracking=True)
    
    # Trailers linked from vehicle
    trailer_1_id = fields.Many2one('fleet.trailer', string='Trailer 1', tracking=True)
    trailer_2_id = fields.Many2one('fleet.trailer', string='Trailer 2', tracking=True)
    trailer_3_id = fields.Many2one('fleet.trailer', string='Trailer 3', tracking=True)
    
    @api.onchange('transporter_id')
    def _onchange_transporter_id(self):
        if not self.transporter_id:
            self.transporter_vehicle_id = False
            self.trailer_1_id = False
            self.trailer_2_id = False
            self.trailer_3_id = False
            # Clear old fields
            self.transport_company = False
            self.horse_registration = False
        else:
            # Update transport_company for backward compatibility
            self.transport_company = self.transporter_id
            if self.transporter_vehicle_id and self.transporter_vehicle_id.transporter_id != self.transporter_id:
                self.transporter_vehicle_id = False
    
    @api.onchange('transporter_vehicle_id')
    def _onchange_transporter_vehicle_id(self):
        if self.transporter_vehicle_id:
            # Load trailers from vehicle
            self.trailer_1_id = self.transporter_vehicle_id.trailer_1_id
            self.trailer_2_id = self.transporter_vehicle_id.trailer_2_id
            self.trailer_3_id = self.transporter_vehicle_id.trailer_3_id
            # Update old fields for backward compatibility
            self.horse_registration = self.transporter_vehicle_id.license_plate
            if self.trailer_1_id:
                self.trailer_registration = self.trailer_1_id.license_plate
            if self.trailer_2_id:
                self.trailer_registration_2 = self.trailer_2_id.license_plate
            if self.trailer_3_id:
                self.trailer_registration_3 = self.trailer_3_id.license_plate
        else:
            self.trailer_1_id = False
            self.trailer_2_id = False
            self.trailer_3_id = False
            self.horse_registration = False
            self.trailer_registration = False
            self.trailer_registration_2 = False
            self.trailer_registration_3 = False
