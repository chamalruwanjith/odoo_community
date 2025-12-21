# -*- coding: utf-8 -*-
# Part of ChaosHub.lk. See LICENSE file for full copyright and licensing details.

{
    'name': 'ChaosHub.lk Website',
    'version': '18.0.3.0.0',
    'category': 'Website/Website',
    'summary': 'Professional Knowledge Hub with SEO, Snippets & Blog Integration',
    'description': """
        ChaosHub.lk - Engineering Clarity from Chaos
        ============================================

        A professional, enterprise-grade Odoo 18 website module with:

        Core Features:
        -------------
        * Website Builder Integration with Custom Snippets
        * SEO Optimization with JSON-LD Structured Data
        * Dark/Light Theme Toggle with localStorage Persistence
        * Dynamic Blog/Knowledge Base with Categories
        * Responsive Design (Mobile, Tablet, Desktop)
        * Performance Optimized Assets (SCSS/JS)
        * Accessibility Compliant (WCAG 2.1 AA)

        Website Builder Snippets:
        ------------------------
        * Hero Section (Multiple Variants)
        * Features Grid
        * Testimonials Carousel
        * Blog/Article Cards
        * Call-to-Action Banners
        * Newsletter Subscription
        * Custom Footer

        SEO & Performance:
        ------------------
        * Automatic Meta Tags Generation
        * Open Graph & Twitter Cards
        * Schema.org Structured Data (Article, Organization)
        * Optimized Sitemap with Blog Posts
        * Lazy Loading Images
        * Fast CSS/JS Bundling

        Pages & Templates:
        -----------------
        * Homepage (Hero, Features, Articles, CTA)
        * Knowledge Base (Filterable, Searchable)
        * Single Article Template (SEO Optimized)
        * About, Services, Contact, Help Pages
        * Custom 404 & Error Pages

        Technical Stack:
        ---------------
        * Python Controllers for Dynamic Content
        * SCSS with Variables & Mixins
        * Modular JavaScript (ES6+)
        * i18n Translation Support
        * Odoo ORM Integration
    """,
    'author': 'ChaosHub.lk',
    'website': 'https://chaoshub.lk',
    'license': 'LGPL-3',
    'depends': [
        'website',
        'website_blog',
        'mass_mailing',  # For newsletter
    ],
    'data': [
        # Security
        'security/ir.model.access.csv',

        # Views (Blog/Website Extensions)
        'views/blog_views.xml',

        # Website Pages
        'views/homepage.xml',
        'views/about.xml',
        'views/services.xml',
        'views/contact.xml',
        'views/knowledge_base.xml',
        'views/article_detail.xml',
        'views/help.xml',

        # Snippets
        'views/snippets/snippets.xml',
        'views/snippets/s_chaoshub_hero.xml',
        'views/snippets/s_chaoshub_features.xml',
        'views/snippets/s_chaoshub_blog_cards.xml',
        'views/snippets/s_chaoshub_cta.xml',
        'views/snippets/s_chaoshub_newsletter.xml',

        # Common Templates
        'views/templates.xml',
        'views/seo_templates.xml',
        'views/seo_enhanced.xml',

        # Website Data
        'data/website_data.xml',
    ],
    'assets': {
        'web.assets_frontend': [
            # SCSS/CSS (loaded in order: variables → mixins → main → features)
            'chaos_chaoshublk/static/src/scss/variables.scss',
            'chaos_chaoshublk/static/src/scss/mixins.scss',
            'chaos_chaoshublk/static/src/scss/chaoshub.scss',
            'chaos_chaoshublk/static/src/scss/snippets.scss',
            'chaos_chaoshublk/static/src/scss/dark_theme.scss',

            # JavaScript
            'chaos_chaoshublk/static/src/js/chaoshub.js',
            'chaos_chaoshublk/static/src/js/snippets.js',
            'chaos_chaoshublk/static/src/js/newsletter.js',
            'chaos_chaoshublk/static/src/js/theme_toggle.js',
        ],
        'website.assets_wysiwyg': [
            # Snippet options for Website Builder
            'chaos_chaoshublk/static/src/js/snippet_options.js',
        ],
        'web.assets_backend': [
            # Backend customizations if needed
        ],
    },
    'images': [
        'static/description/icon.png',
        'static/description/banner.png',
        'static/description/screenshot_homepage.png',
        'static/description/screenshot_snippets.png',
    ],
    'installable': True,
    'application': True,
    'auto_install': False,
    'sequence': 10,
    'price': 0.00,
    'currency': 'USD',
}
