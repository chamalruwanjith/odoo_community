# -*- coding: utf-8 -*-
{
    'name': 'VKD Dropship Management',
    'version': '18.0.1.0.0',
    'category': 'Sales/Purchase',
    'summary': 'Advanced dropship management with PO linking and flexible dropship options',
    'description': """
        VKD Dropship Management
        =======================

        Features:
        ---------
        * Create Sale Orders from existing Purchase Orders
        * Link Sale Orders to specific Purchase Orders to prevent duplicate PO creation
        * Track dropship quantity on Purchase Orders
        * Optional dropship mode per Sale Order (override product default)
        * Smart buttons to view all linked Sale Orders from Purchase Orders

        Scenarios Supported:
        --------------------
        1. Create SO from existing PO - Links to PO instead of creating new one
        2. Direct sale vs Dropship selection - Choose per SO if product supports both
        3. Standard dropship flow - Works with existing Odoo dropship functionality
    """,
    'author': 'VKD',
    'depends': [
        'sale',
        'purchase',
        'stock',
        'sale_stock',
        'purchase_stock',
        'stock_dropshipping',
        'sale_purchase',
        'sale_purchase_stock',
    ],
    'data': [
        'security/ir.model.access.csv',
        'data/res_partner_data.xml',
        'views/res_partner_views.xml',
        'views/sale_order_views.xml',
        'views/purchase_order_views.xml',
    ],
    'installable': True,
    'application': False,
    'auto_install': False,
    'license': 'LGPL-3',
}
