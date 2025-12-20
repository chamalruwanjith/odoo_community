# -*- coding: utf-8 -*-
{
    'name': 'ChaosHub.lk Website',
    'version': '18.0.1.0.0',
    'category': 'Website',
    'summary': 'Modern Knowledge Hub Website for ChaosHub.lk',
    'description': """
        ChaosHub.lk - Engineering Clarity from Chaos
        ============================================

        A modern, SEO-optimized website design system for ChaosHub.lk

        Features:
        ---------
        * Modern responsive design with gradient backgrounds
        * SEO optimized with meta tags and schema.org
        * Complete design system with reusable components
        * 6 main pages: Home, News, Services, About, Contact, Help
        * Mobile-first responsive design
        * Accessibility compliant (WCAG 2.1 AA)
        * Fast loading with optimized assets
        * Knowledge-sharing focused content structure

        Pages Included:
        --------------
        * Homepage - Hero, About, Knowledge Base, Features, Articles, CTA, Newsletter
        * News/Blog - Latest insights and articles
        * Services - Business solutions and offerings
        * About Us - Company story and values
        * Contact - Get in touch form
        * Help/FAQ - Support and common questions
    """,
    'author': 'ChaosHub.lk',
    'website': 'https://chaoshub.lk',
    'license': 'LGPL-3',
    'depends': [
        'website',
        'website_blog',  # For news/blog functionality
    ],
    'data': [
        # Security
        'security/ir.model.access.csv',

        # Website Pages
        'views/homepage.xml',
        'views/about.xml',
        'views/services.xml',
        'views/contact.xml',
        'views/news.xml',
        'views/help.xml',

        # Common Templates & Snippets
        'views/templates.xml',

        # Website Data (Menus, etc.)
        'data/website_data.xml',
    ],
    'assets': {
        'web.assets_frontend': [
            'chaos_chaoshublk/static/src/css/chaoshub.css',
            'chaos_chaoshublk/static/src/js/chaoshub.js',
        ],
    },
    'images': [
        'static/description/icon.png',
        'static/description/banner.png',
    ],
    'installable': True,
    'application': True,
    'auto_install': False,
    'sequence': 10,
}
