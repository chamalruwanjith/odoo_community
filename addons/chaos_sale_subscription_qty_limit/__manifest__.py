# -*- coding: utf-8 -*-
{
    'name': 'Sale Subscription Quantity Limit',
    'version': '18.0.1.0.0',
    'category': 'Sales',
    'summary': 'Limit quantity to 1 for specific subscription upsell products',
    'description': """
Sale Subscription Quantity Limit
=================================
Prevents increasing quantity more than 1 for subscription upsell products
with specific trazet_product_key values (allowExternalAPI, collectPeriod).
    """,
    'author': 'ChaosHub',
    'website': 'https://chaoshub.lk/',
    'license': 'OPL-1',
    'depends': ['sale_subscription', 'portal'],
    'data': [
        'views/templates.xml',
    ],
    'assets': {
        'web.assets_frontend': [
            'chaos_sale_subscription_qty_limit/static/src/js/quantity_limit.js',
        ],
    },
    'installable': True,
    'auto_install': False,
    'application': False,
}
