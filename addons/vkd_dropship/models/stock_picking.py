# -*- coding: utf-8 -*-

from odoo import models, fields, api, _


class StockPicking(models.Model):
    _inherit = 'stock.picking'

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
