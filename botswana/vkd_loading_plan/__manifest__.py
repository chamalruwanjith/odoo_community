# -*- coding: utf-8 -*-
{
    'name': 'Loading Plan',
    'version': '18.0.1.0.0',
    'category': 'Purchase',
    'author': 'VK DATA ApS',
    'website': 'https://vkdata.dk',
    'summary': 'Loading Plan Management for Fuel Suppliers',
    'description': """
        * Supports multiple fuel supplier templates (Namcor, Puma Energy, Vivo, Sasol)
        * Standard template for other suppliers
        * Dynamic field visibility based on supplier
        * Print functionality for loading plans
    """,
    'depends': ['base', 'purchase', 'contacts', 'fleet', 'vkd_fuel_transporter'],
    'data': [
        'security/ir.model.access.csv',
        'views/res_partner_views.xml',
        'views/loading_plan_views.xml',
        'views/purchase_order_views.xml',
        'views/product_template_views.xml',
        'reports/loading_plan_reports.xml',
        'reports/loading_plan_namcor_template.xml',
        'reports/loading_plan_puma_template.xml',
        'reports/loading_plan_vivo_template.xml',
        'reports/loading_plan_sasol_template.xml',
        'reports/loading_plan_standard_template.xml',
        'wizard/loading_plan_report.xml',
        'views/menu_views.xml',
    ],
    'license': 'OPL-1',
    'installable': True,
    'application': False,
    'auto_install': False,
}
