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

    location_rate = fields.Float(string='Location Rate', digits=(16, 2), tracking=True, compute='_compute_location_rate', inverse='_inverse_location_rate', store=True)

    is_transporter_bill = fields.Boolean('Transporter Bill', default=False)
    fuel_bill_id = fields.Many2one('account.move', string='Fuel Bill', readonly=True, help="The Fuel Supplier Bill that generated this Transporter Bill")
    transporter_bill_ids = fields.One2many('account.move', 'fuel_bill_id', string='Transporter Bills', readonly=True)
    transporter_bill_count = fields.Integer(compute='_compute_transporter_bill_count', string='Transporter Bill Count')

    @api.depends('partner_id', 'partner_id.product_id', 'partner_id.product_id.list_price', 'invoice_origin')
    def _compute_location_rate(self):
        """Compute location rate from partner or from related sale order"""
        for move in self:
            if move.invoice_origin:
                # Try to get from sale order
                sale_order = self.env['sale.order'].search([('name', '=', move.invoice_origin)], limit=1)
                if sale_order and sale_order.location_rate:
                    move.location_rate = sale_order.location_rate
                    continue
            # Otherwise use partner's location rate
            if move.partner_id and move.partner_id.product_id:
                move.location_rate = move.partner_id.product_id.list_price
            else:
                move.location_rate = 0.0

    def _inverse_location_rate(self):
        """Allow manual override of location rate"""
        for move in self:
            move.location_rate = move.location_rate

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

    @api.model_create_multi
    def create(self, vals_list):
        """Override to copy transporter details from SO/PO when creating invoice"""
        moves = super(AccountMove, self).create(vals_list)
        for move in moves:
            if move.invoice_origin and not move.transporter_id:
                # Try to get transporter from sale order
                sale_order = self.env['sale.order'].search([('name', '=', move.invoice_origin)], limit=1)
                if sale_order and sale_order.transporter_id:
                    move.write({
                        'transporter_id': sale_order.transporter_id.id,
                        'transporter_vehicle_id': sale_order.transporter_vehicle_id.id if sale_order.transporter_vehicle_id else False,
                        'trailer_1_id': sale_order.trailer_1_id.id if sale_order.trailer_1_id else False,
                        'trailer_2_id': sale_order.trailer_2_id.id if sale_order.trailer_2_id else False,
                        'trailer_3_id': sale_order.trailer_3_id.id if sale_order.trailer_3_id else False,
                    })
                    continue

                # Try to get transporter from purchase order
                purchase_order = self.env['purchase.order'].search([('name', '=', move.invoice_origin)], limit=1)
                if purchase_order and purchase_order.transporter_id:
                    move.write({
                        'transporter_id': purchase_order.transporter_id.id,
                        'transporter_vehicle_id': purchase_order.transporter_vehicle_id.id if purchase_order.transporter_vehicle_id else False,
                        'trailer_1_id': purchase_order.trailer_1_id.id if purchase_order.trailer_1_id else False,
                        'trailer_2_id': purchase_order.trailer_2_id.id if purchase_order.trailer_2_id else False,
                        'trailer_3_id': purchase_order.trailer_3_id.id if purchase_order.trailer_3_id else False,
                    })
        return moves
    
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
        """
        Create transporter bills from vendor bill (fuel bill)

        Logic:
        1. Get all purchase orders from this vendor bill
        2. For each PO, find all related pickings (receipts and dropship deliveries)
        3. For each delivery/receipt with transporter, create a line in transporter bill
        4. Formula: Delivered Quantity * Transporter Location Rate
        5. Group all lines by transporter into one bill per transporter per PO
        """
        for move in self:
            # Get purchase orders from this vendor bill
            purchase_orders = move.invoice_line_ids.mapped('purchase_line_id.order_id')
            if not purchase_orders:
                raise UserError(_("No purchase orders found for this vendor bill. Cannot create transporter bill."))

            # Group deliveries by transporter
            transporter_deliveries = {}

            for po in purchase_orders:
                # Get all related pickings (incoming receipts and dropship deliveries)
                pickings = self.env['stock.picking'].search([
                    '|',
                    ('purchase_id', '=', po.id),  # Incoming receipts from PO
                    ('sale_id.source_purchase_order_id', '=', po.id),  # Dropship deliveries from linked SOs
                    ('state', '=', 'done'),  # Only validated pickings
                    ('transporter_id', '!=', False),  # Only pickings with transporter
                ])

                for picking in pickings:
                    transporter = picking.transporter_id
                    if not transporter:
                        continue

                    # Get location rate (should be on picking or calculate from customer)
                    location_rate = picking.location_rate
                    if not location_rate:
                        # Try to get from customer's product
                        if picking.partner_id and picking.partner_id.product_id:
                            location_rate = picking.partner_id.product_id.list_price
                        else:
                            continue  # Skip if no location rate

                    # Calculate delivered quantity (sum of all move lines)
                    delivered_qty = sum(picking.move_ids.filtered(lambda m: m.state == 'done').mapped('quantity'))

                    if delivered_qty <= 0:
                        continue

                    # Get or create product from customer (for invoice line)
                    product = picking.partner_id.product_id if picking.partner_id else None
                    if not product:
                        # Use a default service product if customer doesn't have location rate product
                        product = self.env['product.product'].search([
                            ('is_location_rate', '=', True),
                            ('type', '=', 'service')
                        ], limit=1)
                        if not product:
                            raise UserError(_(f"No location rate product found for delivery {picking.name}. "
                                            "Please set up location rate product on customer or create a default one."))

                    # Group by transporter
                    if transporter not in transporter_deliveries:
                        transporter_deliveries[transporter] = []

                    # Add delivery-wise entry
                    delivery_type = 'Dropship Delivery' if picking.picking_type_code == 'outgoing' else 'Warehouse Receipt'
                    transporter_deliveries[transporter].append({
                        'product_id': product.id,
                        'quantity': delivered_qty,
                        'price_unit': location_rate,
                        'name': f"{delivery_type} - {picking.name} (Customer: {picking.partner_id.name if picking.partner_id else 'N/A'})",
                        'tax_ids': [(6, 0, product.supplier_taxes_id.ids)],
                    })

            # Create one transporter bill per transporter
            for transporter, delivery_lines in transporter_deliveries.items():
                if not delivery_lines:
                    continue

                invoice_lines = [(0, 0, line) for line in delivery_lines]

                self.env['account.move'].create({
                    'move_type': 'in_invoice',
                    'is_transporter_bill': True,
                    'fuel_bill_id': move.id,
                    'partner_id': transporter.id,
                    'invoice_date': fields.Date.context_today(self),
                    'invoice_line_ids': invoice_lines,
                    'ref': f"Transporter Bill for {move.name}",
                })

