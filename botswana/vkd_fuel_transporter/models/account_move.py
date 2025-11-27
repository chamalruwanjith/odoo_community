# -*- coding: utf-8 -*-
from odoo import models, fields, api
from odoo.exceptions import UserError


class AccountMove(models.Model):
    _inherit = 'account.move'

    transporter_id = fields.Many2one('res.partner', string='Transporter', domain=[('is_transporter', '=', True)], tracking=True)
    transporter_vehicle_id = fields.Many2one('fleet.vehicle', string='Vehicle (Reg Number)', domain="[('transporter_id', '=', transporter_id)]", tracking=True)

    trailer_1_id = fields.Many2one('fleet.trailer', string='Trailer 1', tracking=True)
    trailer_2_id = fields.Many2one('fleet.trailer', string='Trailer 2', tracking=True)
    trailer_3_id = fields.Many2one('fleet.trailer', string='Trailer 3', tracking=True)

    is_transporter_bill = fields.Boolean('Transporter Bill', default=False)
    fuel_bill_id = fields.Many2one('account.move', string='Fuel Bill', readonly=True, help="The Fuel Supplier Bill that generated this Transporter Bill")
    transporter_bill_ids = fields.One2many('account.move', 'fuel_bill_id', string='Transporter Bills', readonly=True)
    transporter_bill_count = fields.Integer(compute='_compute_transporter_bill_count', string='Transporter Bill Count')

    @api.depends('transporter_bill_ids')
    def _compute_transporter_bill_count(self):
        for move in self:
            move.transporter_bill_count = len(move.transporter_bill_ids)

    def action_view_transporter_bills(self):
        self.ensure_one()
        return {
            'name': 'Transporter Bills',
            'type': 'ir.actions.act_window',
            'res_model': 'account.move',
            'view_mode': 'list,form',
            'domain': [('id', 'in', self.transporter_bill_ids.ids)],
            'context': {'default_fuel_bill_id': self.id, 'default_move_type': 'in_invoice'},
        }
    
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

    def action_create_transporter_bill(self):
        for move in self:
            purchase_orders = move.invoice_line_ids.purchase_line_id.order_id
            if not purchase_orders:
                continue

            sale_orders = purchase_orders.mapped('linked_sale_order_ids')

            relevant_sos = sale_orders.filtered(lambda so: so.partner_id and so.location_rate)
            
            # Group by transporter to create bills
            transporter_so_map = {}
            for so in relevant_sos:
                if so.transporter_id not in transporter_so_map:
                    transporter_so_map[so.transporter_id] = []
                transporter_so_map[so.transporter_id].append(so)
            
            for transporter, sos in transporter_so_map.items():
                invoice_lines = []
                for so in sos:
                    # Product from SO's Customer (partner_id)
                    product = so.partner_id.product_id
                    if not product:
                        raise UserError(f"Customer {so.partner_id.name} on Sale Order {so.name} does not have a 'Location Rate' product defined.")
                    
                    # Calculate delivered quantity
                    delivered_qty = sum(so.order_line.mapped('qty_delivered'))
                    
                    if delivered_qty <= 0:
                        continue

                    invoice_lines.append((0, 0, {
                        'product_id': product.id,
                        'quantity': delivered_qty,
                        'price_unit': so.location_rate,
                        'name': f"Transport for {so.name}",
                        'tax_ids': [(6, 0, product.supplier_taxes_id.ids)],
                    }))
                
                if invoice_lines:
                    self.env['account.move'].create({
                        'move_type': 'in_invoice',
                        'is_transporter_bill': True,
                        'fuel_bill_id': move.id,
                        'partner_id': transporter.id,
                        'invoice_date': fields.Date.context_today(self),
                        'invoice_line_ids': invoice_lines,
                        'ref': f"Transporter Bill for {move.name}",
                    })

