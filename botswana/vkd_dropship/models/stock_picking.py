# -*- coding: utf-8 -*-
from odoo import models, fields, api, _
from odoo.tools import float_compare


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
        res = super(StockPicking, self).button_validate()

        for picking in self:
            if picking.is_dropship:
                picking._update_po_dropship_quantities()

        return res

    def _update_po_dropship_quantities(self):
        self.ensure_one()

        purchase_orders = self.move_ids.mapped('purchase_line_id.order_id')

        if purchase_orders:
            purchase_orders.mapped('order_line')._compute_dropship_quantities()

    def _check_backorder(self):
        """
        check backorder with expected_to_receive for incoming receipts with dropship

        For incoming receipts from PO with linked dropship orders:
        - Check if picked quantity < expected_to_receive (instead of < product_uom_qty)
        - This prevents creating backorders for already dropshipped quantities

        For all other pickings:
        - Use standard backorder logic
        """

        prec = self.env["decimal.precision"].precision_get("Product Unit of Measure")
        backorder_pickings = self.browse()

        for picking in self:
            if picking.picking_type_id.create_backorder == 'never':
                continue

            if picking.picking_type_id.create_backorder not in ('ask', 'always'):
                continue

            if picking.picking_type_code == 'incoming' and picking.has_dropship_from_po:
                needs_backorder = False
                for move in picking.move_ids:
                    if move.state == 'cancel':
                        continue

                    if (move.purchase_line_id and
                        move.location_dest_id.usage == 'internal'):

                        # Only check if there's still quantity expected
                        if move.expected_to_receive > 0:
                            if (not move.picked or
                                float_compare(move._get_picked_quantity(), move.expected_to_receive, precision_digits=prec) < 0):
                                needs_backorder = True
                                break
                    else:
                        if ((move.product_uom_qty and not move.picked) or
                            float_compare(move._get_picked_quantity(), move.product_uom_qty, precision_digits=prec) < 0):
                            needs_backorder = True
                            break

                if needs_backorder:
                    backorder_pickings |= picking
            else:
                if any(
                    (move.product_uom_qty and not move.picked) or
                    float_compare(move._get_picked_quantity(), move.product_uom_qty, precision_digits=prec) < 0
                    for move in picking.move_ids
                    if move.state != 'cancel'
                ):
                    backorder_pickings |= picking

        return backorder_pickings


