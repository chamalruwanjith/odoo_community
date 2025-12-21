# -*- coding: utf-8 -*-
# Part of ChaosHub.lk. See LICENSE file for full copyright and licensing details.

import json
from datetime import datetime
from odoo import http
from odoo.http import request
from odoo.addons.website.controllers.main import Website
from odoo.addons.http_routing.models.ir_http import slug


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

    @http.route(['/article/<model("blog.post"):post>'], type='http', auth='public', website=True, sitemap=True)
    def article_detail(self, post, **kwargs):
        """Single article view with SEO optimization"""
        if not post.can_access_from_current_website():
            raise request.not_found()

        # Generate JSON-LD structured data
        structured_data = {
            "@context": "https://schema.org",
            "@type": "Article",
            "headline": post.name,
            "description": post.subtitle or post.teaser[:160] if post.teaser else '',
            "image": request.website.image_url(post, 'cover_properties') if post.cover_properties else '',
            "datePublished": post.create_date.isoformat() if post.create_date else '',
            "dateModified": post.write_date.isoformat() if post.write_date else '',
            "author": {
                "@type": "Person",
                "name": post.author_id.name if post.author_id else "ChaosHub Team"
            },
            "publisher": {
                "@type": "Organization",
                "name": "ChaosHub.lk",
                "logo": {
                    "@type": "ImageObject",
                    "url": request.website.image_url(request.website.company_id, 'logo')
                }
            }
        }

        # Related articles
        related_posts = request.env['blog.post'].sudo().search([
            ('id', '!=', post.id),
            ('website_published', '=', True),
            ('tag_ids', 'in', post.tag_ids.ids)
        ], limit=3, order='create_date desc')

        values = {
            'post': post,
            'related_posts': related_posts,
            'structured_data': json.dumps(structured_data),
            'page_name': 'article',
            'main_object': post,
        }
        return request.render('chaos_chaoshublk.article_detail_page', values)

    @http.route(['/sitemap.xml'], type='http', auth="public", website=True, sitemap=False)
    def sitemap_xml(self, **kwargs):
        """Enhanced sitemap with blog posts"""
        pages = request.website.enumerate_pages()

        # Add blog posts to sitemap
        posts = request.env['blog.post'].sudo().search([('website_published', '=', True)])
        for post in posts:
            loc = '/article/%s' % slug(post)
            pages.append({
                'loc': loc,
                'lastmod': post.write_date.strftime('%Y-%m-%d') if post.write_date else datetime.now().strftime('%Y-%m-%d'),
                'priority': 0.8,
                'changefreq': 'weekly'
            })

        return request.render('website.sitemap_xml', {'pages': pages}, headers={'Content-Type': 'application/xml; charset=utf-8'})


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
