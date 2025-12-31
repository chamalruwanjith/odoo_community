# -*- coding: utf-8 -*-
{
    'name': 'Website Sale Quantity Limit for Upsell',
    'version': '18.0.1.0.0',
    'category': 'Website/Website',
    'summary': 'Limit quantity to 1 for upsell/optional products in cart',
    'description': """
Website Sale Quantity Limit
============================

This module prevents customers from adding more than 1 quantity of upsell/optional products.

Features:
---------
* Limit maximum quantity to 1 for optional/upsell products
* Disable (+) button when quantity reaches 1
* Prevent manual quantity input above 1
* Visual feedback for quantity restrictions
    """,
    'author': 'ChaosHub',
    'website': 'https://chaoshub.lk/',
    'depends': ['website_sale'],
    'data': [
        'views/templates.xml',
    ],
    'assets': {
        'web.assets_frontend': [
            'chaos_website_sale_qty_limit/static/src/js/website_sale_qty_limit.js',
        ],
    },
    'installable': True,
    'auto_install': False,
    'application': False,
    'license': 'OPL-1',
}
