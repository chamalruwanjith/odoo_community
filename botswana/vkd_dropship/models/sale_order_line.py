from odoo import models, fields, api, _
from odoo.exceptions import UserError


class SaleOrderLine(models.Model):
    _inherit = 'sale.order.line'

    is_dropship = fields.Boolean(
        string='Is Dropship',
        compute='_compute_is_dropship',
        store=True,
        help='Indicates if this line will use dropship process'
    )
    source_purchase_line_id = fields.Many2one(
        'purchase.order.line',
        string='Source PO Line',
        help='Link to specific PO line from source PO'
    )

    @api.depends('order_id.is_dropship_order', 'product_id', 'order_id.source_purchase_order_id')
    def _compute_is_dropship(self):
        for line in self:
            if line.order_id.is_dropship_order and line._is_product_dropshippable():
                line.is_dropship = True
            elif line.order_id.source_purchase_order_id:
                line.is_dropship = True
            else:
                line.is_dropship = False

    def _is_product_dropshippable(self):
        self.ensure_one()
        if not self.product_id:
            return False

        dropship_route = self.env.ref('stock_dropshipping.route_drop_shipping', raise_if_not_found=False)
        if not dropship_route:
            return False

        # Check if product has dropship route
        return dropship_route in self.product_id.route_ids or dropship_route in self.product_id.categ_id.route_ids

    def _action_launch_stock_rule(self, previous_product_uom_qty=False):
        """
         handle custom dropship logic:
        - If SO is linked to source PO, create dropship picking directly without new PO
        - If is_dropship_order is False, skip dropship route even if product has it

        """

        lines_to_process = self.env['sale.order.line']
        lines_skip_procurement = self.env['sale.order.line']

        for line in self:
            # SO linked to existing PO - handle separately
            if line.order_id.source_purchase_order_id and line.is_dropship:
                lines_skip_procurement |= line
                # Create dropship picking directly from source PO
                line._create_dropship_from_source_po()
            elif not line.order_id.is_dropship_order and line._is_product_dropshippable():
                # Temporarily remove dropship route from product to force standard delivery
                lines_to_process |= line
            else:
                # Standard processing
                lines_to_process |= line

        # Process lines that go through normal procurement
        if lines_to_process:
            # For lines where we want to skip dropship route, we need to handle specially
            lines_force_standard = lines_to_process.filtered(
                lambda l: not l.order_id.is_dropship_order and l._is_product_dropshippable()
            )

            if lines_force_standard:
                # Process with dropship route temporarily disabled
                result = lines_force_standard._process_lines_without_dropship_route(previous_product_uom_qty)

            # Process remaining lines normally
            lines_normal = lines_to_process - lines_force_standard
            if lines_normal:
                result = super(SaleOrderLine, lines_normal)._action_launch_stock_rule(previous_product_uom_qty)

        return True

    def _process_lines_without_dropship_route(self, previous_product_uom_qty=False):
        dropship_route = self.env.ref('stock_dropshipping.route_drop_shipping', raise_if_not_found=False)

        for line in self:
            original_product_routes = line.product_id.route_ids
            original_categ_routes = line.product_id.categ_id.route_ids

            # Temporarily remove dropship route
            if dropship_route:
                line.product_id.route_ids = original_product_routes - dropship_route
                line.product_id.categ_id.route_ids = original_categ_routes - dropship_route

            try:
                # Call standard procurement
                super(SaleOrderLine, line)._action_launch_stock_rule(previous_product_uom_qty)
            finally:
                # Restore original routes
                if dropship_route:
                    line.product_id.route_ids = original_product_routes
                    line.product_id.categ_id.route_ids = original_categ_routes

        return True

    def _create_dropship_from_source_po(self):
        """
        Create dropship picking directly from source PO without creating new PO.
        SO created from existing PO
        """
        self.ensure_one()

        if not self.order_id.source_purchase_order_id:
            return

        source_po = self.order_id.source_purchase_order_id

        matching_po_line = source_po.order_line.filtered(
            lambda pol: pol.product_id == self.product_id and pol.product_qty >= self.product_uom_qty
        )[:1]

        if not matching_po_line:
            raise UserError(_(
                'Cannot find matching product "%s" in source PO "%s" with sufficient quantity. '
                'Available quantity in PO: %s, Requested: %s'
            ) % (
                self.product_id.name,
                source_po.name,
                sum(source_po.order_line.filtered(lambda pol: pol.product_id == self.product_id).mapped('product_qty')),
                self.product_uom_qty
            ))

        self.source_purchase_line_id = matching_po_line.id

        dropship_picking_type = self.env['stock.picking.type'].search([
            ('code', '=', 'dropship'),
            ('company_id', '=', self.company_id.id)
        ], limit=1)

        if not dropship_picking_type:
            raise UserError(_('Dropship picking type not found. Please install stock_dropshipping module.'))

        existing_picking = self.env['stock.picking'].search([
            ('sale_id', '=', self.order_id.id),
            ('picking_type_id', '=', dropship_picking_type.id),
            ('state', 'not in', ['done', 'cancel'])
        ], limit=1)

        if not existing_picking:
            picking_vals = {
                'picking_type_id': dropship_picking_type.id,
                'partner_id': self.order_id.partner_shipping_id.id,
                'origin': self.order_id.name,
                'location_id': source_po.partner_id.property_stock_supplier.id,
                'location_dest_id': self.order_id.partner_shipping_id.property_stock_customer.id,
                'sale_id': self.order_id.id,
                'purchase_id': source_po.id,
            }
            picking = self.env['stock.picking'].create(picking_vals)
        else:
            picking = existing_picking

        move_vals = {
            'name': self.product_id.name,
            'product_id': self.product_id.id,
            'product_uom_qty': self.product_uom_qty,
            'product_uom': self.product_uom.id,
            'picking_id': picking.id,
            'location_id': source_po.partner_id.property_stock_supplier.id,
            'location_dest_id': self.order_id.partner_shipping_id.property_stock_customer.id,
            'partner_id': self.order_id.partner_shipping_id.id,
            'sale_line_id': self.id,
            'purchase_line_id': matching_po_line.id,
            'origin': self.order_id.name,
        }
        move = self.env['stock.move'].create(move_vals)

        if move.state == 'draft':
            move._action_confirm()

        if picking.state == 'draft':
            picking.action_confirm()

        return picking