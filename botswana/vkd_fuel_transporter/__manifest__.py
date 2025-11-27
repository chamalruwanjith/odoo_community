# -*- coding: utf-8 -*-
{
    'name': 'Fuel Transporter',
    'version': '18.0.1.2.0',
    'category': 'Fleet',
    'author': 'VK DATA ApS',
    'website': 'https://vkdata.dk',
    'summary': 'Transporter Management with Vehicles and Trailers',
    'description': """
        Transporter Management Module
        * Link transporters to fleet vehicles
        * Partner can have multiple vehicles
        * Automatic linking when creating vehicles from Fleet module
        * Support for multiple trailers (up to 3) per vehicle
        * Integration with purchase orders, sales orders, stock pickings
        * Integration with loading plans, GRN, delivery orders, bills and invoices
        * Enhanced vehicle-partner relationship with uniqueness constraint
        * Improved vehicle creation from Fleet module with automatic partner linking
        * Better validation to ensure one vehicle belongs to only one partner
    """,
    'depends': [
        'base',
        'fleet',
        'contacts',
        'purchase',
        'sale',
        'stock',
        'account',
    ],
    'data': [
        'security/ir.model.access.csv',
        'data/sequence_data.xml',
        'data/product_template_data.xml',
        'views/fleet_vehicle_views.xml',
        'views/fleet_trailer_views.xml',
        'views/res_partner_views.xml',
        'views/purchase_order_views.xml',
        'views/sale_order_views.xml',
        'views/stock_picking_views.xml',
        'views/account_move_views.xml',
        'views/product_template_views.xml',
        'views/menu_views.xml',
    ],
    'installable': True,
    'auto_install': False,
    'application': False,
    'license': 'OPL-1',
}

