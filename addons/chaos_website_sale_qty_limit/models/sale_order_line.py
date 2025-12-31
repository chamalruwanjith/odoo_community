# -*- coding: utf-8 -*-

from odoo import models


class SaleOrderLine(models.Model):
    _inherit = 'sale.order.line'

    def _is_upsell_line(self):
        """
        Check if this order line is an upsell/optional product.
        Optional products have a linked_line_id set.
        """
        self.ensure_one()
        return bool(self.linked_line_id)
