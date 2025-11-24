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
        1. Use expected_to_receive for backorder logic on INCOMING receipts with dropship
        2. Update dropship quantities when dropship moves are done

        IMPORTANT: Only affects incoming receipts, NOT dropship pickings (supplier->customer)
        """
        # For INCOMING receipts with dropship, temporarily set product_uom_qty to expected_to_receive
        # This makes backorder calculation use the correct expected quantity
        # Only for receipts going to company locations, NOT for dropship moves
        for move in self:
            # Check: Must be incoming receipt (to company location), NOT dropship (to customer)
            if (move.picking_id and
                move.picking_id.picking_type_code == 'incoming' and
                move.picking_id.has_dropship_from_po and
                move.purchase_line_id and
                move.expected_to_receive > 0 and
                move.location_dest_id.usage == 'internal'):  # Going to warehouse, not customer
                # Temporarily set demand to expected qty for backorder calculation
                move.product_uom_qty = move.expected_to_receive

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
