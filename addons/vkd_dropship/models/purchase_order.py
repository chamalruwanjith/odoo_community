# -*- coding: utf-8 -*-

from odoo import models, fields, api, _


class PurchaseOrder(models.Model):
    _inherit = 'purchase.order'

    dropship_quantity_total = fields.Float(
        string='Total Dropship Quantity',
        compute='_compute_dropship_quantities',
        store=True,
        help='Total quantity that has been dropshipped from this PO'
    )
    dropship_quantity_reserved = fields.Float(
        string='Reserved Dropship Quantity',
        compute='_compute_dropship_quantities',
        store=True,
        help='Quantity reserved for dropship (linked to SOs but not yet delivered)'
    )
    remaining_quantity = fields.Float(
        string='Remaining Quantity',
        compute='_compute_dropship_quantities',
        store=True,
        help='Quantity remaining to be received or dropshipped'
    )
    linked_sale_order_ids = fields.One2many(
        'sale.order',
        'source_purchase_order_id',
        string='Linked Sale Orders',
        help='Sale orders created from this PO'
    )
    linked_sale_order_count = fields.Integer(
        string='Linked SO Count',
        compute='_compute_linked_sale_order_count',
        help='Number of sale orders linked to this PO'
    )

    @api.depends('linked_sale_order_ids')
    def _compute_linked_sale_order_count(self):
        for order in self:
            order.linked_sale_order_count = len(order.linked_sale_order_ids)

    @api.depends('order_line.dropship_qty_delivered', 'order_line.dropship_qty_reserved', 'order_line.product_qty', 'order_line.qty_received')
    def _compute_dropship_quantities(self):
        for order in self:
            order.dropship_quantity_total = sum(order.order_line.mapped('dropship_qty_delivered'))
            order.dropship_quantity_reserved = sum(order.order_line.mapped('dropship_qty_reserved'))
            total_ordered = sum(order.order_line.mapped('product_qty'))
            total_received = sum(order.order_line.mapped('qty_received'))
            order.remaining_quantity = total_ordered - order.dropship_quantity_total - total_received

    def action_view_linked_sale_orders(self):
        """
        Smart button action to view all linked sale orders
        """
        self.ensure_one()
        action = self.env.ref('sale.action_orders').read()[0]
        action['domain'] = [('source_purchase_order_id', '=', self.id)]
        action['context'] = {'default_source_purchase_order_id': self.id}
        return action

    def action_create_sale_order(self):
        """
        Action to create a new sale order from this PO with auto-populated lines
        """
        self.ensure_one()

        # Find the dropship customer (placeholder customer)
        dropship_customer = self.env['res.partner'].search([
            ('is_dropship_customer', '=', True)
        ], limit=1)

        if not dropship_customer:
            # If no dropship customer exists, use current user's partner
            dropship_customer = self.env.user.partner_id

        # Create a new SO with this PO as source
        sale_order = self.env['sale.order'].create({
            'partner_id': dropship_customer.id,
            'source_purchase_order_id': self.id,
            'is_dropship_order': True,
        })

        # Auto-populate SO lines from PO lines (products only)
        for po_line in self.order_line:
            # Only add product lines (skip services, consumables if needed)
            if po_line.product_id and po_line.product_id.detailed_type == 'product':
                # Create SO line
                self.env['sale.order.line'].create({
                    'order_id': sale_order.id,
                    'product_id': po_line.product_id.id,
                    'product_uom_qty': po_line.product_qty,
                    'product_uom': po_line.product_uom.id,
                    'price_unit': po_line.price_unit,  # You can adjust pricing logic
                    'source_purchase_line_id': po_line.id,
                })

        # Copy transporter and vehicle details from PO to SO (if vkd_fuel_transporter is installed)
        if hasattr(sale_order, 'copy_transporter_from_purchase'):
            sale_order.copy_transporter_from_purchase(self)

        # Return action to open the new SO
        return {
            'type': 'ir.actions.act_window',
            'name': _('Create Sale Order from PO'),
            'res_model': 'sale.order',
            'res_id': sale_order.id,
            'view_mode': 'form',
            'target': 'current',
        }


class PurchaseOrderLine(models.Model):
    _inherit = 'purchase.order.line'

    dropship_qty_delivered = fields.Float(
        string='Dropship Delivered Qty',
        compute='_compute_dropship_quantities',
        store=True,
        digits='Product Unit of Measure',
        help='Quantity delivered via dropship'
    )
    dropship_qty_reserved = fields.Float(
        string='Dropship Reserved Qty',
        compute='_compute_dropship_quantities',
        store=True,
        digits='Product Unit of Measure',
        help='Quantity reserved for dropship (in SO but not yet delivered)'
    )
    source_sale_line_ids = fields.One2many(
        'sale.order.line',
        'source_purchase_line_id',
        string='Source Sale Lines',
        help='Sale order lines linked to this PO line'
    )

    @api.depends('move_ids.state', 'move_ids.product_uom_qty', 'source_sale_line_ids', 'source_sale_line_ids.product_uom_qty')
    def _compute_dropship_quantities(self):
        """
        Compute dropship quantities:
        - dropship_qty_delivered: Quantity from dropship moves that are done
        - dropship_qty_reserved: Quantity from linked SO lines not yet delivered
        """
        for line in self:
            # Get dropship moves (supplier -> customer)
            dropship_moves = line.move_ids.filtered(
                lambda m: m.location_id.usage == 'supplier' and m.location_dest_id.usage == 'customer'
            )

            # Delivered quantity (done dropship moves)
            delivered_moves = dropship_moves.filtered(lambda m: m.state == 'done')
            line.dropship_qty_delivered = sum(delivered_moves.mapped('product_uom_qty'))

            # Reserved quantity (linked SO lines not yet delivered)
            reserved_qty = 0
            for sale_line in line.source_sale_line_ids:
                # Check if sale line has pending dropship moves
                pending_moves = dropship_moves.filtered(
                    lambda m: m.sale_line_id == sale_line and m.state not in ['done', 'cancel']
                )
                if pending_moves:
                    reserved_qty += sum(pending_moves.mapped('product_uom_qty'))
                else:
                    # If no moves yet, count the full SO line qty
                    if sale_line.order_id.state in ['draft', 'sent']:
                        reserved_qty += sale_line.product_uom_qty

            line.dropship_qty_reserved = reserved_qty
