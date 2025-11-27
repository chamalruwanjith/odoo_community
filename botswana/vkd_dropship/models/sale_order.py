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
        string='Purchase Order',
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
        if self.source_purchase_order_id:
            self.is_dropship_order = True

    def action_view_source_purchase_order(self):
        self.ensure_one()
        return {
            'type': 'ir.actions.act_window',
            'name': _('Source Purchase Order'),
            'res_model': 'purchase.order',
            'res_id': self.source_purchase_order_id.id,
            'view_mode': 'form',
            'target': 'current',
        }

    def action_confirm(self):
        for order in self:
            if order.partner_id.is_dropship_customer:
                raise UserError(_(
                    'Cannot confirm Sale Order "%s".\n\n'
                    'Please select the actual customer before confirming this order.'
                ) % (order.name))

        return super(SaleOrder, self).action_confirm()

