# -*- coding: utf-8 -*-
from odoo import models, fields, api


class FleetTrailer(models.Model):
    _name = 'fleet.trailer'
    _description = 'Fleet Trailer'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _order = 'name'

    name = fields.Char(string='Trailer Name', required=True, tracking=True)
    license_plate = fields.Char(string='Trailer Registration Number', tracking=True, help='Registration number of the trailer', copy=False)
    vin_sn = fields.Char(string='Chassis Number', help='Unique chassis/VIN number', copy=False)

    company_id = fields.Many2one('res.company', string='Company', default=lambda self: self.env.company)
    active = fields.Boolean(string='Active', default=True, tracking=True)

    capacity = fields.Float(string='Capacity (Liters)', help='Maximum capacity in liters')
    trailer_type = fields.Selection([
        ('tanker', 'Tanker'),
    ], string='Trailer Type', default='tanker', tracking=True)

    vehicle_id = fields.Many2one('fleet.vehicle', string='Vehicle', tracking=True, help='Primary vehicle this trailer is linked to')

    notes = fields.Text(string='Notes')
    
    _sql_constraints = [
        ('license_plate_unique', 'UNIQUE(license_plate, company_id)', 'Registration number must be unique per company!')
    ]
