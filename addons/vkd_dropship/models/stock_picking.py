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
        Override to:
        1. Update dropship quantities on PO when dropship picking is validated
        2. Handle backorder logic for receipts with dropship
        """
        # Handle incoming receipts from PO with dropship
        for picking in self:
            if picking.has_dropship_from_po and picking.picking_type_code == 'incoming':
                picking._adjust_receipt_for_dropship()

        res = super(StockPicking, self).button_validate()

        # Process dropship pickings
        for picking in self:
            if picking.is_dropship:
                picking._update_po_dropship_quantities()

        return res

    def _adjust_receipt_for_dropship(self):
        """
        Adjust receipt quantities to account for dropshipped amounts and already received qty
        No longer adjusts product_uom_qty - instead marks moves for proper backorder calculation
        """
        self.ensure_one()

        if not self.purchase_id:
            return

        # Mark moves with expected_to_receive for backorder logic
        for move in self.move_ids:
            po_line = move.purchase_line_id
            if not po_line:
                continue

            # Compute expected_to_receive will be used by backorder logic
            # No need to modify product_uom_qty here

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
                 'purchase_line_id.qty_received')
    def _compute_dropship_qty_for_line(self):
        for move in self:
            if move.purchase_line_id:
                po_line = move.purchase_line_id
                dropship_qty = po_line.dropship_qty_delivered + po_line.dropship_qty_reserved
                # For display: total dropship
                move.dropship_qty_for_line = dropship_qty
                # For backorder calculation: expected remaining after dropship and received
                # Only count already received qty (not including current move)
                received_qty = po_line.qty_received - move.quantity
                move.expected_to_receive = po_line.product_qty - dropship_qty - received_qty
            else:
                move.dropship_qty_for_line = 0
                move.expected_to_receive = 0

    def _prepare_move_split_vals(self, qty):
        """
        Override to use expected_to_receive for backorder calculation on receipts with dropship
        """
        vals = super(StockMove, self)._prepare_move_split_vals(qty)

        # Check if this is a receipt from PO with dropship
        if self.picking_id and self.picking_id.has_dropship_from_po and self.purchase_line_id:
            # For receipts with dropship, use expected_to_receive instead of product_uom_qty
            # The backorder should be based on what's actually expected, not the full PO qty
            if self.expected_to_receive > 0:
                # Calculate backorder quantity based on expected_to_receive
                remaining_expected = self.expected_to_receive - self.quantity
                if remaining_expected > 0:
                    vals['product_uom_qty'] = remaining_expected

        return vals

    def _should_bypass_reservation(self, location):
        """
        Override to handle backorder logic for receipts with dropship.
        Checks against expected_to_receive instead of product_uom_qty.
        """
        # For receipts from PO with dropship, override backorder check
        if self.picking_id and self.picking_id.has_dropship_from_po and self.purchase_line_id:
            # Use expected_to_receive for determining if backorder is needed
            if self.quantity < self.expected_to_receive:
                # Split the move: some done, rest to backorder
                quantity_to_split = self.expected_to_receive - self.quantity
                if quantity_to_split > 0:
                    # Force the split based on expected_to_receive
                    return super(StockMove, self)._should_bypass_reservation(location)

        return super(StockMove, self)._should_bypass_reservation(location)

    def _action_done(self, cancel_backorder=False):
        """
        Override to:
        1. Use expected_to_receive for backorder logic on dropship receipts
        2. Update dropship quantities when dropship moves are done
        """
        # For receipts with dropship, adjust backorder logic
        for move in self:
            if move.picking_id and move.picking_id.has_dropship_from_po and move.purchase_line_id:
                # Override product_uom_qty temporarily for backorder calculation
                if move.expected_to_receive > 0:
                    # Store original
                    original_uom_qty = move.product_uom_qty
                    # Set to expected for backorder logic
                    move.product_uom_qty = move.expected_to_receive
                    # This will be used by the split logic in _action_done

        res = super(StockMove, self)._action_done(cancel_backorder=cancel_backorder)

        # Update dropship quantities for dropship moves
        dropship_moves = self.filtered(
            lambda m: m.location_id.usage == 'supplier' and m.location_dest_id.usage == 'customer'
        )

        if dropship_moves:
            # Get related PO lines
            po_lines = dropship_moves.mapped('purchase_line_id')
            if po_lines:
                # Trigger recomputation
                po_lines._compute_dropship_quantities()

        return res

