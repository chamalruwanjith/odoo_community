# -*- coding: utf-8 -*-
from odoo import models, fields, api, _
from odoo.exceptions import ValidationError


class FleetVehicle(models.Model):
    _inherit = 'fleet.vehicle'

    transporter_id = fields.Many2one(
        'res.partner', 
        string='Transporter/Customer',
        tracking=True, 
        help='Transport company/transporter this vehicle belongs to. One vehicle can only belong to one transporter.',
        ondelete='restrict'
    )

    trailer_1_id = fields.Many2one('fleet.trailer', string='Trailer 1', tracking=True)
    trailer_2_id = fields.Many2one('fleet.trailer', string='Trailer 2', tracking=True)
    trailer_3_id = fields.Many2one('fleet.trailer', string='Trailer 3', tracking=True)
    
    trailer_count = fields.Integer(string='Number of Trailers', compute='_compute_trailer_count', store=True)
    trailer_ids = fields.Many2many('fleet.trailer', compute='_compute_trailer_ids', string='All Trailers')
    
    @api.depends('trailer_1_id', 'trailer_2_id', 'trailer_3_id')
    def _compute_trailer_count(self):
        for vehicle in self:
            count = 0
            if vehicle.trailer_1_id:
                count += 1
            if vehicle.trailer_2_id:
                count += 1
            if vehicle.trailer_3_id:
                count += 1
            vehicle.trailer_count = count
    
    @api.depends('trailer_1_id', 'trailer_2_id', 'trailer_3_id')
    def _compute_trailer_ids(self):
        for vehicle in self:
            trailers = self.env['fleet.trailer']
            if vehicle.trailer_1_id:
                trailers |= vehicle.trailer_1_id
            if vehicle.trailer_2_id:
                trailers |= vehicle.trailer_2_id
            if vehicle.trailer_3_id:
                trailers |= vehicle.trailer_3_id
            vehicle.trailer_ids = trailers
    
    @api.constrains('trailer_1_id', 'trailer_2_id', 'trailer_3_id')
    def _check_trailer_uniqueness(self):
        """Ensure the same trailer is not assigned multiple times to one vehicle"""
        for vehicle in self:
            trailers = []
            if vehicle.trailer_1_id:
                trailers.append(vehicle.trailer_1_id.id)
            if vehicle.trailer_2_id:
                trailers.append(vehicle.trailer_2_id.id)
            if vehicle.trailer_3_id:
                trailers.append(vehicle.trailer_3_id.id)
            
            if len(trailers) != len(set(trailers)):
                raise ValidationError(_('Cannot assign the same trailer multiple times to a vehicle!'))
    
    @api.constrains('transporter_id')
    def _check_transporter_single_assignment(self):
        """Ensure one vehicle can only belong to one transporter
        This constraint ensures data integrity at the database level"""
        for vehicle in self:
            if vehicle.transporter_id:
                # Check if this vehicle is already assigned to a different transporter
                # This happens when trying to link the same vehicle to multiple partners
                other_assignments = self.search([
                    ('id', '!=', vehicle.id),
                    ('transporter_id', '!=', False),
                    ('transporter_id', '!=', vehicle.transporter_id.id),
                    '|', ('license_plate', '=', vehicle.license_plate),
                         ('vin_sn', '=', vehicle.vin_sn)
                ])
                if other_assignments:
                    raise ValidationError(_(
                        'This vehicle is already assigned to transporter "%s". '
                        'A vehicle can only belong to one transporter at a time.'
                    ) % other_assignments[0].transporter_id.name)
