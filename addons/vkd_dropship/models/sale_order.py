# -*- coding: utf-8 -*-

from odoo import models, fields, api, _
from odoo.exceptions import UserError


class SaleOrder(models.Model):
    _inherit = 'sale.order'

    is_dropship_order = fields.Boolean(
        string='Is Dropship Order',
        default=False,
        help='If checked, this sale order will use dropship process. '
             'If unchecked, standard delivery process will be used even if product has dropship route.'
    )
    source_purchase_order_id = fields.Many2one(
        'purchase.order',
        string='Source Purchase Order',
        domain="[('state', 'in', ['draft', 'sent', 'to approve', 'purchase'])]",
        help='Link this SO to an existing PO. When set, no new PO will be created and '
             'dropship will be directly from this PO.'
    )
    linked_to_purchase = fields.Boolean(
        string='Linked to PO',
        compute='_compute_linked_to_purchase',
        store=True,
        help='Indicates if this SO is linked to a source PO'
    )

    @api.depends('source_purchase_order_id')
    def _compute_linked_to_purchase(self):
        for order in self:
            order.linked_to_purchase = bool(order.source_purchase_order_id)

    @api.onchange('is_dropship_order')
    def _onchange_is_dropship_order(self):
        """
        When is_dropship_order is changed, validate product compatibility
        """
        if self.is_dropship_order:
            # Check if any order lines have products that cannot be dropshipped
            non_dropship_products = self.order_line.filtered(
                lambda line: line.product_id and not line._is_product_dropshippable()
            )
            if non_dropship_products:
                product_names = ', '.join(non_dropship_products.mapped('product_id.name'))
                return {
                    'warning': {
                        'title': _('Non-Dropship Products'),
                        'message': _('The following products are not configured for dropship: %s', product_names)
                    }
                }

    @api.onchange('source_purchase_order_id')
    def _onchange_source_purchase_order_id(self):
        """
        When source PO is selected, automatically set is_dropship_order to True
        """
        if self.source_purchase_order_id:
            self.is_dropship_order = True

    def action_view_source_purchase_order(self):
        """
        Action to view the source purchase order
        """
        self.ensure_one()
        return {
            'type': 'ir.actions.act_window',
            'name': _('Source Purchase Order'),
            'res_model': 'purchase.order',
            'res_id': self.source_purchase_order_id.id,
            'view_mode': 'form',
            'target': 'current',
        }


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
        """
        Determine if this line should be dropshipped based on:
        1. SO is_dropship_order flag
        2. Product has dropship route
        3. SO is linked to a source PO
        """
        for line in self:
            # If SO is explicitly marked as dropship and product supports it
            if line.order_id.is_dropship_order and line._is_product_dropshippable():
                line.is_dropship = True
            # If linked to source PO, it's dropship
            elif line.order_id.source_purchase_order_id:
                line.is_dropship = True
            else:
                line.is_dropship = False

    def _is_product_dropshippable(self):
        """
        Check if product can be dropshipped (has dropship route configured)
        """
        self.ensure_one()
        if not self.product_id:
            return False

        # Get dropship route
        dropship_route = self.env.ref('stock_dropshipping.route_drop_shipping', raise_if_not_found=False)
        if not dropship_route:
            return False

        # Check if product has dropship route
        return dropship_route in self.product_id.route_ids or dropship_route in self.product_id.categ_id.route_ids

    def _action_launch_stock_rule(self, previous_product_uom_qty=False):
        """
        Override to handle custom dropship logic:
        - If SO is linked to source PO, create dropship picking directly without new PO
        - If is_dropship_order is False, skip dropship route even if product has it
        """
        # Filter lines based on dropship logic
        lines_to_process = self.env['sale.order.line']
        lines_skip_procurement = self.env['sale.order.line']

        for line in self:
            # Scenario 1 & 2: SO linked to existing PO - handle separately
            if line.order_id.source_purchase_order_id and line.is_dropship:
                lines_skip_procurement |= line
                # Create dropship picking directly from source PO
                line._create_dropship_from_source_po()
            # Scenario 2 & 3: Not dropship order, use standard process
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
        """
        Process lines forcing standard delivery route (bypass dropship)
        """
        # Get dropship route
        dropship_route = self.env.ref('stock_dropshipping.route_drop_shipping', raise_if_not_found=False)

        for line in self:
            # Store original routes
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
        This is for Scenario 1: SO created from existing PO
        """
        self.ensure_one()

        if not self.order_id.source_purchase_order_id:
            return

        source_po = self.order_id.source_purchase_order_id

        # Find matching PO line based on product
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

        # Link SO line to PO line
        self.source_purchase_line_id = matching_po_line.id

        # Create stock move for dropship
        # Get dropship picking type
        dropship_picking_type = self.env['stock.picking.type'].search([
            ('code', '=', 'dropship'),
            ('company_id', '=', self.company_id.id)
        ], limit=1)

        if not dropship_picking_type:
            raise UserError(_('Dropship picking type not found. Please install stock_dropshipping module.'))

        # Create or find existing dropship picking for this SO
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

        # Create stock move
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
        self.env['stock.move'].create(move_vals)

        return picking
