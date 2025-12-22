# -*- coding: utf-8 -*-
{
    'name': 'Disable Database Expiration',
    'version': '18.0.1.0.2',
    'category': 'Technical',
    'summary': 'Remove database expiration warnings and bypass social media subscription checks',
    'description': """
Disable Database Expiration & Social Media IAP
==============================================

This module automatically:
- Extends database expiration date to 50 years from now
- Clears expiration warnings
- Prevents expiration notifications
- **Bypasses social media IAP subscription checks**
- Allows using your own OAuth apps for social media

Features:
- Works with Facebook, LinkedIn, Twitter, Instagram, YouTube
- Provides helpful configuration messages
- No subscription required for social media features

Setup for Social Media:
1. Get OAuth credentials from each platform (Facebook, LinkedIn, etc.)
2. Add them to System Parameters: Settings → Technical → Parameters → System Parameters
3. Link your social accounts normally

Example Parameters:
- social.facebook_app_id
- social.facebook_client_secret
- social.linkedin_client_id
- social.linkedin_client_secret

Useful for:
- Development databases
- Testing environments
- On-premise installations
- Using own social media API keys
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
