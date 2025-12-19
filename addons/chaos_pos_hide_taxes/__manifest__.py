# -*- coding: utf-8 -*-
{
    'name': 'POS Hide Taxes',
    'version': '18.0.1.0.0',
    'category': 'Point of Sale',
    'summary': 'Hide untaxed amount and taxes from POS receipt',
    'description': """
        POS Receipt Customization
        =========================
        This module adds a configurable option to hide taxes from POS receipts:
        * Untaxed amount (total without tax)
        * Tax breakdown section
        * Tax details

        The setting can be enabled/disabled per Point of Sale configuration.
        Multi-company support: Each POS config has its own setting.
    """,
    'author': 'Chaos',
    'website': '',
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
    'installable': True,
    'auto_install': False,
    'application': False,
    'license': 'LGPL-3',
}
