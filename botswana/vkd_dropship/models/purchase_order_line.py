from odoo import models, fields, api, _


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