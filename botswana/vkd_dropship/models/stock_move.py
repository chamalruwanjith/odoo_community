# -*- coding: utf-8 -*-
from odoo import models, fields, api, _
from odoo.exceptions import UserError
from odoo.tools import float_compare


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

                received_qty = po_line.qty_received
                if received_qty >= 0:
                    move.expected_to_receive = po_line.product_qty - received_qty - po_line.dropship_qty_reserved
                else:
                    move.expected_to_receive = po_line.product_qty - dropship_qty
            else:
                move.dropship_qty_for_line = 0
                move.expected_to_receive = 0

    def _action_done(self, cancel_backorder=False):
        """
        1. Validate quantity doesn't exceed expected_to_receive for incoming receipts with dropship
        2. Update dropship quantities when dropship moves are done

        IMPORTANT: Backorder logic handled in StockPicking._check_backorder()
        """
        # Validate quantity for incoming receipts with dropship from PO
        for move in self:
            if (move.picking_id and
                move.picking_id.picking_type_code == 'incoming' and
                move.picking_id.has_dropship_from_po and
                move.purchase_line_id and
                move.location_dest_id.usage == 'internal'):

                if move.expected_to_receive > 0 and move.quantity > move.expected_to_receive:
                    raise UserError(_(
                        'Cannot receive more than expected quantity!\n\n'
                        'Product: %s\n'
                        'Expected to receive: %s %s\n'
                        'Trying to receive: %s %s\n\n'
                        'This PO has linked dropship orders. The expected quantity accounts for:\n'
                        '- Ordered: %s\n'
                        '- Dropshipped: %s (Delivered: %s, Reserved: %s)\n'
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
                        move.expected_to_receive,
                    ))

        res = super(StockMove, self)._action_done(cancel_backorder=cancel_backorder)

        dropship_moves = self.filtered(
            lambda m: m.location_id.usage == 'supplier' and m.location_dest_id.usage == 'customer'
        )

        if dropship_moves:
            po_lines = dropship_moves.mapped('purchase_line_id')
            if po_lines:
                po_lines._compute_dropship_quantities()

        return res

    def _create_backorder(self):
        """
        use expected_to_receive for split decision on incoming receipts with dropship

        For incoming receipts from PO with linked dropship:
        - Compare quantity vs expected_to_receive (instead of vs product_uom_qty)
        - This prevents creating backorder moves for already dropshipped quantities

        For all other moves:
        - Use standard logic
        """

        backorder_moves_vals = []
        rounding = self.env['decimal.precision'].precision_get('Product Unit of Measure')

        for move in self:
            if (move.picking_id and
                move.picking_id.picking_type_code == 'incoming' and
                move.picking_id.has_dropship_from_po and
                move.purchase_line_id and
                move.location_dest_id.usage == 'internal'):

                # Use expected_to_receive instead of product_uom_qty for backorder check
                if move.expected_to_receive > 0 and float_compare(move.quantity, move.expected_to_receive, precision_digits=rounding) < 0:
                    # Need to create backorder for remaining expected quantity
                    qty_split = move.product_uom._compute_quantity(
                        move.expected_to_receive - move.quantity,
                        move.product_id.uom_id,
                        rounding_method='HALF-UP'
                    )
                    new_move_vals = move._split(qty_split)
                    backorder_moves_vals += new_move_vals
                # If expected_to_receive <= 0 or quantity >= expected_to_receive, no backorder needed
            else:
                # Standard logic: compare with product_uom_qty
                if float_compare(move.quantity, move.product_uom_qty, precision_digits=rounding) < 0:
                    qty_split = move.product_uom._compute_quantity(
                        move.product_uom_qty - move.quantity,
                        move.product_id.uom_id,
                        rounding_method='HALF-UP'
                    )
                    new_move_vals = move._split(qty_split)
                    backorder_moves_vals += new_move_vals

        backorder_moves = self.env['stock.move'].create(backorder_moves_vals)
        backorder_moves.with_context(bypass_entire_pack=True, bypass_procurement_creation=True)._action_confirm(merge=False)
        return backorder_moves