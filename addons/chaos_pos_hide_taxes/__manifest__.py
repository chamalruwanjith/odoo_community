# -*- coding: utf-8 -*-
{
    'name': 'POS Receipt Hide Taxes',
    'version': '18.0.1.0.0',
    'category': 'Point of Sale',
    'sequence': 10,
    'summary': 'Hide untaxed amount and taxes from POS receipt',
    'description': """
POS Receipt Customization
=========================

This module hides the following from POS receipts:
* Untaxed amount (total without tax)
* Tax breakdown section
* Tax details

The receipt will only show the final total amount.

Key Features:
-------------
* Configurable per Point of Sale
* Hide tax breakdown section
* Hide untaxed amounts (subtotals)
* Maintain total amount display
* Multi-company support
* Easy checkbox configuration
* No coding required

Configuration:
--------------
Point of Sale → Configuration → Settings → Bills & Receipts → Hide Taxes on Receipt
    """,
    'author': 'ChaosHub',
    'maintainer': 'ChaosHub',
    'website': 'https://chaoshub.lk/',
    'support': 'https://github.com/chaoshub-git/odoo-apps/issues',
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
    'price': 25.00,
    'currency': 'USD',
    'installable': True,
    'auto_install': False,
    'application': False,
    'license': 'OPL-1',
    'live_test_url': '',
}
