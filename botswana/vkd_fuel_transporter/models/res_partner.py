# -*- coding: utf-8 -*-
from odoo import models, fields, api


class ResPartner(models.Model):
    _inherit = 'res.partner'

    is_transporter = fields.Boolean(
        string='Is a Transporter', 
        help='Check this box if this contact is a transporter/transport company'
    )
    
    transporter_vehicle_ids = fields.One2many(
        'fleet.vehicle', 
        'transporter_id', 
        string='Vehicles', 
        help='Vehicles owned by this transporter. One partner can have multiple vehicles, but each vehicle can only belong to one partner.'
    )
    
    transporter_vehicle_count = fields.Integer(
        string='Vehicle Count', 
        compute='_compute_transporter_vehicle_count',
        store=True,
    )

    product_id = fields.Many2one('product.product', string='Location Rate', domain="[('type', '=', 'service'), ('is_location_rate', '=', True)]")
    
    @api.depends('transporter_vehicle_ids')
    def _compute_transporter_vehicle_count(self):
        for partner in self:
            partner.transporter_vehicle_count = len(partner.transporter_vehicle_ids)
    
    def action_view_transporter_vehicles(self):
        self.ensure_one()
        return {
            'name': f'Vehicles - {self.name}',
            'type': 'ir.actions.act_window',
            'res_model': 'fleet.vehicle',
            'view_mode': 'list,form',
            'domain': [('transporter_id', '=', self.id)],
            'context': {
                'default_transporter_id': self.id,
                'search_default_transporter_id': self.id,
            }
        }
