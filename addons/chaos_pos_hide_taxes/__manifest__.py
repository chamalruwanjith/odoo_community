# -*- coding: utf-8 -*-
{
    'name': 'POS Hide Taxes on Receipt',
    'version': '18.0.1.0.0',
    'category': 'Point of Sale',
    'sequence': 10,
    'summary': 'Hide tax breakdown and untaxed amounts from POS receipts - Cleaner receipt format',
    'description': """
POS Receipt Tax Configuration
==============================

Hide tax information from Point of Sale receipts for a cleaner, simplified format.

Key Features:
-------------
* Configurable per Point of Sale
* Hide tax breakdown section
* Hide untaxed amounts (subtotals)
* Maintain total amount display
* Multi-company support
* Easy checkbox configuration
* No coding required

Perfect for businesses that want simpler receipts without detailed tax information.

Configuration:
--------------
Point of Sale → Configuration → Settings → Bills & Receipts → Hide Taxes on Receipt
    """,
    'author': 'Chaos',
    'maintainer': 'Chamal Ruwanjith',
    'website': 'https://github.com/chamalruwanjith/odoo_community',
    'support': 'https://github.com/chamalruwanjith/odoo_community/issues',
    'depends': ['point_of_sale'],
    'data': [
        'views/res_config_settings_views.xml',
    ],
    'assets': {
        'point_of_sale._assets_pos': [
            'chaos_pos_hide_taxes/static/src/app/models/pos_order.js',
            'chaos_pos_hide_taxes/static/src/app/screens/receipt_screen/receipt/order_receipt.xml',
        ],
    },
    'images': [
        'static/description/banner.png',
        'static/description/icon.png',
        'static/description/screenshot_config.png',
        'static/description/screenshot_receipt_comparison.png',
        'static/description/screenshot_settings.png',
    ],
    'installable': True,
    'auto_install': False,
    'application': False,
    'price': 0.00,
    'currency': 'USD',
    'license': 'LGPL-3',
    'live_test_url': '',
}
