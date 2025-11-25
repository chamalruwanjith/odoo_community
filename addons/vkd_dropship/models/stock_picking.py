# -*- coding: utf-8 -*-

from odoo import models, fields, api, _


class StockPicking(models.Model):
    _inherit = 'stock.picking'

    has_dropship_from_po = fields.Boolean(
        string='Has Dropship from PO',
        compute='_compute_has_dropship_from_po',
        store=True,
        help='This receipt is from a PO that has dropship orders'
    )
    po_dropship_info = fields.Char(
        string='Dropship Info',
        compute='_compute_po_dropship_info',
        help='Information about dropshipped quantities from source PO'
    )

    @api.depends('purchase_id', 'purchase_id.linked_sale_order_ids', 'picking_type_code')
    def _compute_has_dropship_from_po(self):
        for picking in self:
            # Only for incoming pickings (receipts) from PO
            if picking.picking_type_code == 'incoming' and picking.purchase_id:
                po = picking.purchase_id
                # Check if PO has linked dropship SOs
                picking.has_dropship_from_po = bool(po.linked_sale_order_ids)
            else:
                picking.has_dropship_from_po = False

    @api.depends('purchase_id', 'purchase_id.dropship_quantity_total',
                 'purchase_id.dropship_quantity_reserved', 'has_dropship_from_po')
    def _compute_po_dropship_info(self):
        for picking in self:
            if picking.has_dropship_from_po and picking.purchase_id:
                po = picking.purchase_id
                dropship_qty = po.dropship_quantity_total + po.dropship_quantity_reserved
                picking.po_dropship_info = f"Dropshipped: {dropship_qty:.2f} (Delivered: {po.dropship_quantity_total:.2f}, Reserved: {po.dropship_quantity_reserved:.2f})"
            else:
                picking.po_dropship_info = False

    def button_validate(self):
        """
        Override to update dropship quantities on PO when dropship picking is validated
        """
        res = super(StockPicking, self).button_validate()

        # Process dropship pickings
        for picking in self:
            if picking.is_dropship:
                picking._update_po_dropship_quantities()

        return res

    def _update_po_dropship_quantities(self):
        """
        Update dropship_quantity fields on related PO when dropship is validated
        """
        self.ensure_one()

        # Get related purchase orders through moves
        purchase_orders = self.move_ids.mapped('purchase_line_id.order_id')

        # Trigger recomputation of dropship quantities
        if purchase_orders:
            purchase_orders.mapped('order_line')._compute_dropship_quantities()


class StockMove(models.Model):
    _inherit = 'stock.move'

    dropship_qty_for_line = fields.Float(
        string='Dropship Qty',
        compute='_compute_dropship_qty_for_line',
        help='Quantity dropshipped from the related PO line'
    )
    expected_to_receive = fields.Float(
        string='Expected to Receive',
        compute='_compute_dropship_qty_for_line',
        help='Quantity expected to be received (after accounting for dropship)'
    )

    @api.depends('purchase_line_id', 'purchase_line_id.dropship_qty_delivered',
                 'purchase_line_id.dropship_qty_reserved', 'purchase_line_id.product_qty',
                 'purchase_line_id.qty_received', 'quantity')
    def _compute_dropship_qty_for_line(self):
        for move in self:
            if move.purchase_line_id:
                po_line = move.purchase_line_id
                dropship_qty = po_line.dropship_qty_delivered + po_line.dropship_qty_reserved
                move.dropship_qty_for_line = dropship_qty

                # For backorder calculation: expected remaining after dropship and already received
                # Don't count current move's quantity in received_qty to get accurate remaining
                received_qty = po_line.qty_received - move.quantity
                move.expected_to_receive = po_line.product_qty - dropship_qty - received_qty
            else:
                move.dropship_qty_for_line = 0
                move.expected_to_receive = 0

    def _action_done(self, cancel_backorder=False):
        """
        Override to:
        1. Validate quantity doesn't exceed expected_to_receive for incoming receipts with dropship
        2. Update dropship quantities when dropship moves are done

        IMPORTANT: Does NOT modify product_uom_qty. Backorder logic handled in _split()
        """
        # Validate quantity for incoming receipts with dropship from PO
        for move in self:
            if (move.picking_id and
                move.picking_id.picking_type_code == 'incoming' and
                move.picking_id.has_dropship_from_po and
                move.purchase_line_id and
                move.location_dest_id.usage == 'internal'):

                if move.expected_to_receive > 0 and move.quantity > move.expected_to_receive:
                    from odoo.exceptions import UserError
                    raise UserError(_(
                        'Cannot receive more than expected quantity!\n\n'
                        'Product: %s\n'
                        'Expected to receive: %s %s\n'
                        'Trying to receive: %s %s\n\n'
                        'This PO has linked dropship orders. The expected quantity accounts for:\n'
                        '- Ordered: %s\n'
                        '- Dropshipped: %s (Delivered: %s, Reserved: %s)\n'
                        '- Already received: %s\n'
                        '- Remaining to receive: %s'
                    ) % (
                        move.product_id.display_name,
                        move.expected_to_receive,
                        move.product_uom.name,
                        move.quantity,
                        move.product_uom.name,
                        move.purchase_line_id.product_qty,
                        move.dropship_qty_for_line,
                        move.purchase_line_id.dropship_qty_delivered,
                        move.purchase_line_id.dropship_qty_reserved,
                        move.purchase_line_id.qty_received - move.quantity,
                        move.expected_to_receive,
                    ))

        res = super(StockMove, self)._action_done(cancel_backorder=cancel_backorder)

        # Update dropship quantities for dropship moves (supplier -> customer)
        dropship_moves = self.filtered(
            lambda m: m.location_id.usage == 'supplier' and m.location_dest_id.usage == 'customer'
        )

        if dropship_moves:
            po_lines = dropship_moves.mapped('purchase_line_id')
            if po_lines:
                po_lines._compute_dropship_quantities()

        return res

    def _split(self, qty, restrict_partner_id=False):
        """
        Override to use expected_to_receive for backorder calculation on incoming receipts with dropship

        Standard logic: Split if quantity < product_uom_qty
        Custom logic: For receipts with dropship, split if quantity < expected_to_receive
        """
        # For INCOMING receipts with dropship from PO
        # Check backorder against expected_to_receive instead of product_uom_qty
        if (self.picking_id and
            self.picking_id.picking_type_code == 'incoming' and
            self.picking_id.has_dropship_from_po and
            self.purchase_line_id and
            self.expected_to_receive > 0 and
            self.location_dest_id.usage == 'internal'):  # Going to warehouse, not customer

            # Calculate remaining based on expected_to_receive
            remaining_qty = self.expected_to_receive - qty

            if remaining_qty > 0:
                # Create backorder with remaining quantity based on expected
                # Temporarily swap product_uom_qty to make split work correctly
                original_uom_qty = self.product_uom_qty
                self.product_uom_qty = self.expected_to_receive

                try:
                    new_move = super(StockMove, self)._split(qty, restrict_partner_id)
                finally:
                    # Restore original
                    self.product_uom_qty = original_uom_qty

                return new_move
            else:
                # No backorder needed
                return self.env['stock.move']

        # Standard flow for all other cases
        return super(StockMove, self)._split(qty, restrict_partner_id)
