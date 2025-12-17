# -*- coding: utf-8 -*-
{
    'name': 'Disable Database Expiration',
    'version': '18.0.1.0.0',
    'category': 'Technical',
    'summary': 'Remove database expiration warnings and extend expiration date',
    'description': """
Disable Database Expiration
============================

This module automatically:
- Extends database expiration date to 50 years from now
- Clears expiration warnings
- Prevents expiration notifications

Useful for:
- Development databases
- Testing environments
- On-premise installations
    """,
    'author': 'Custom',
    'depends': ['base', 'web'],
    'data': [
        'data/ir_cron.xml',
    ],
    'installable': True,
    'application': False,
    'auto_install': False,
    'license': 'LGPL-3',
}
