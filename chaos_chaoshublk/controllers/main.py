# -*- coding: utf-8 -*-
# Part of ChaosHub.lk. See LICENSE file for full copyright and licensing details.

import json
from datetime import datetime
from odoo import http
from odoo.http import request


class ChaosHubWebsite(http.Controller):
    """ChaosHub Website Controller for SEO and dynamic content"""

    @http.route(['/knowledge', '/knowledge/page/<int:page>'], type='http', auth='public', website=True, sitemap=True)
    def knowledge_base(self, page=1, category=None, search=None, **kwargs):
        """Knowledge base listing with categories and search"""
        Blog = request.env['blog.post']
        categories = request.env['blog.tag'].sudo().search([])

        domain = [('website_published', '=', True)]
        if category:
            domain.append(('tag_ids.name', '=', category))
        if search:
            domain.append(('name', 'ilike', search))

        # Pagination
        posts_per_page = 12
        total_posts = Blog.sudo().search_count(domain)
        pager = request.website.pager(
            url='/knowledge',
            total=total_posts,
            page=page,
            step=posts_per_page,
            url_args={'category': category, 'search': search}
        )

        posts = Blog.sudo().search(domain, limit=posts_per_page, offset=pager['offset'], order='create_date desc')

        values = {
            'posts': posts,
            'categories': categories,
            'pager': pager,
            'current_category': category,
            'search_query': search,
            'page_name': 'knowledge_base',
        }
        return request.render('chaos_chaoshublk.knowledge_base_page', values)



class NewsletterController(http.Controller):
    """Newsletter subscription handler"""

    @http.route(['/newsletter/subscribe'], type='json', auth='public', website=True, methods=['POST'])
    def subscribe_newsletter(self, email, **kwargs):
        """Handle newsletter subscription via AJAX"""
        if not email:
            return {'success': False, 'message': 'Email is required'}

        # Create mailing list contact
        try:
            MailingContact = request.env['mailing.contact'].sudo()
            existing = MailingContact.search([('email', '=', email)], limit=1)

            if not existing:
                MailingContact.create({
                    'email': email,
                    'name': email.split('@')[0],
                })

            return {'success': True, 'message': 'Successfully subscribed!'}
        except Exception as e:
            return {'success': False, 'message': 'Subscription failed. Please try again.'}


class SEOController(http.Controller):
    """SEO helpers and meta tag generation"""

    def _get_default_meta(self):
        """Get default SEO meta tags"""
        return {
            'title': 'ChaosHub.lk - Engineering Clarity from Chaos',
            'description': 'ChaosHub transforms complex business and technology concepts into clear, practical knowledge. Learn ERP, accounting, digital transformation, and modern business insights.',
            'keywords': 'ERP, accounting, digital transformation, business management, Odoo, knowledge base',
            'og_title': 'ChaosHub.lk - Your Journey Starts Here',
            'og_description': 'Transform complex business concepts into clear, practical knowledge.',
            'og_image': '/chaos_chaoshublk/static/src/img/og-image.jpg',
            'twitter_card': 'summary_large_image',
        }

    def _get_page_meta(self, page_name, **kwargs):
        """Get page-specific SEO meta tags"""
        meta_data = {
            'homepage': {
                'title': 'ChaosHub.lk - Your Journey Starts Here | ERP & Business Knowledge',
                'description': 'ChaosHub transforms complex business and technology concepts into clear, practical knowledge. Learn ERP, accounting, digital transformation, and modern business insights.',
            },
            'knowledge_base': {
                'title': 'Knowledge Base | ChaosHub.lk',
                'description': 'Browse our comprehensive library of articles, guides, and tutorials on ERP, accounting, and business management.',
            },
            'about': {
                'title': 'About ChaosHub | Engineering Clarity from Chaos',
                'description': 'Learn about ChaosHub\'s mission to simplify ERP, accounting, and business management concepts for professionals and entrepreneurs.',
            },
            'services': {
                'title': 'Our Services | ChaosHub.lk',
                'description': 'Discover our comprehensive business solutions including ERP consulting, accounting services, and digital transformation support.',
            },
            'contact': {
                'title': 'Contact Us | ChaosHub.lk',
                'description': 'Get in touch with ChaosHub. We\'re here to help you navigate complex business and technology challenges.',
            },
        }

        default_meta = self._get_default_meta()
        page_meta = meta_data.get(page_name, {})

        return {**default_meta, **page_meta, **kwargs}
