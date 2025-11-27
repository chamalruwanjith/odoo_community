# -*- coding: utf-8 -*-
from odoo import models, fields, api, _
from odoo.exceptions import UserError


class PurchaseOrder(models.Model):
    _inherit = 'purchase.order'

    dropship_quantity_total = fields.Float(
        string='Total Dropship Quantity',
        compute='_compute_dropship_quantities',
        store=True,
        help='Total quantity that has been dropshipped from this PO'
    )
    dropship_quantity_reserved = fields.Float(
        string='Reserved Dropship Quantity',
        compute='_compute_dropship_quantities',
        store=True,
        help='Quantity reserved for dropship (linked to SOs but not yet delivered)'
    )
    remaining_quantity = fields.Float(
        string='Remaining Quantity',
        compute='_compute_dropship_quantities',
        store=True,
        help='Quantity remaining to be received or dropshipped'
    )
    linked_sale_order_ids = fields.One2many(
        'sale.order',
        'source_purchase_order_id',
        string='Linked Sale Orders',
        help='Sale orders created from this PO'
    )
    linked_sale_order_count = fields.Integer(
        string='Linked SO Count',
        compute='_compute_linked_sale_order_count',
        help='Number of sale orders linked to this PO'
    )

    @api.depends('linked_sale_order_ids')
    def _compute_linked_sale_order_count(self):
        for order in self:
            order.linked_sale_order_count = len(order.linked_sale_order_ids)

    @api.depends('order_line.dropship_qty_delivered', 'order_line.dropship_qty_reserved', 'order_line.product_qty', 'order_line.qty_received')
    def _compute_dropship_quantities(self):
        for order in self:
            order.dropship_quantity_total = sum(order.order_line.mapped('dropship_qty_delivered'))
            order.dropship_quantity_reserved = sum(order.order_line.mapped('dropship_qty_reserved'))
            total_ordered = sum(order.order_line.mapped('product_qty'))
            total_received = sum(order.order_line.mapped('qty_received'))
            order.remaining_quantity = total_ordered - order.dropship_quantity_total - total_received


    def action_create_sale_order(self):
        self.ensure_one()
        total_received = 0
        total_ordered = 0
        for order in self:
            total_ordered = sum(order.order_line.mapped('product_qty'))
            total_received = sum(order.order_line.mapped('qty_received'))
        if total_ordered == total_received:
            raise UserError(_("Cannot create sale order already received"))

        dropship_customer = self.env['res.partner'].search([
            ('is_dropship_customer', '=', True)
        ], limit=1)

        if not dropship_customer:
            dropship_customer = self.env.user.partner_id

        sale_order = self.env['sale.order'].create({
            'partner_id': dropship_customer.id,
            'source_purchase_order_id': self.id,
            'is_dropship_order': True,
        })

        for po_line in self.order_line:
            if po_line.product_id:
                # Create SO line
                self.env['sale.order.line'].create({
                    'order_id': sale_order.id,
                    'product_id': po_line.product_id.id,
                    'product_uom': po_line.product_uom.id,
                    'source_purchase_line_id': po_line.id,
                })

        return {
            'type': 'ir.actions.act_window',
            'name': _('Create Sale Order from PO'),
            'res_model': 'sale.order',
            'res_id': sale_order.id,
            'view_mode': 'form',
            'target': 'current',
        }

