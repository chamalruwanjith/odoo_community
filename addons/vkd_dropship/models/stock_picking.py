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
        Adjust receipt quantities to account for dropshipped amounts
        Prevents unnecessary backorder creation
        """
        self.ensure_one()

        if not self.purchase_id:
            return

        po = self.purchase_id

        # For each move in the receipt
        for move in self.move_ids:
            po_line = move.purchase_line_id
            if not po_line:
                continue

            # Get dropshipped quantity for this PO line
            dropship_qty = po_line.dropship_qty_delivered + po_line.dropship_qty_reserved

            # Expected to receive = ordered - dropshipped
            expected_to_receive = po_line.product_qty - dropship_qty

            # If demand quantity hasn't been manually changed and is still the full PO qty
            # Adjust it to the expected amount
            if move.product_uom_qty == po_line.product_qty and dropship_qty > 0:
                # Update the demand to exclude dropship qty
                move.product_uom_qty = expected_to_receive

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
                 'purchase_line_id.dropship_qty_reserved', 'purchase_line_id.product_qty')
    def _compute_dropship_qty_for_line(self):
        for move in self:
            if move.purchase_line_id:
                po_line = move.purchase_line_id
                move.dropship_qty_for_line = po_line.dropship_qty_delivered + po_line.dropship_qty_reserved
                move.expected_to_receive = po_line.product_qty - move.dropship_qty_for_line
            else:
                move.dropship_qty_for_line = 0
                move.expected_to_receive = 0

    def _action_done(self, cancel_backorder=False):
        """
        Override to ensure dropship quantities are updated when moves are done
        """
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

