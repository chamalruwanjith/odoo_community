# -*- coding: utf-8 -*-
{
    'name': 'Sale Project Subtask Automation',
    'version': '18.0.1.0.0',
    'category': 'Sales/Sales',
    'summary': 'Automatically create subtasks from product templates when sale orders are confirmed',
    'description': """
Sale Project Subtask Automation
================================
This module extends the sale_project functionality to automatically create subtasks
based on product configuration when sale orders are confirmed.

Key Features:
-------------
* Configure subtask templates on products
* Automatic subtask creation when tasks are generated from sale orders
* Subtasks inherit parent task properties (project, partner, sale order)
* Configurable subtask name, sequence, allocated hours, and description
* Seamless integration with existing sale_project workflow
    """,
    'author': 'Your Company',
    'website': 'https://www.yourcompany.com',
    'license': 'LGPL-3',
    'depends': [
        'sale_project',
        'project',
    ],
    'data': [
        'security/ir.model.access.csv',
        'views/product_template_views.xml',
        'views/product_subtask_template_views.xml',
    ],
    'demo': [],
    'installable': True,
    'application': False,
    'auto_install': False,
}
