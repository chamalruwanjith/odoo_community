# -*- coding: utf-8 -*-
# Part of ChaosHub.lk. See LICENSE file for full copyright and licensing details.

from odoo import models, fields, api


class Website(models.Model):
    _inherit = 'website'

    def _prepare_seo_meta(self, page_name='', **kwargs):
        """Prepare SEO meta tags for a page"""
        meta = {
            'og_type': 'website',
            'og_site_name': 'ChaosHub.lk',
            'twitter_card': 'summary_large_image',
            'twitter_site': '@chaoshub',
        }

        page_meta = {
            'homepage': {
                'title': 'ChaosHub.lk - Your Journey Starts Here | ERP & Business Knowledge',
                'description': 'Transform complex business concepts into clear, practical knowledge. Learn ERP, accounting, and digital transformation.',
                'keywords': 'ERP, accounting, digital transformation, Odoo, business management',
            },
            'knowledge': {
                'title': 'Knowledge Base | Articles & Guides | ChaosHub.lk',
                'description': 'Browse comprehensive guides on ERP systems, accounting, and business management.',
                'keywords': 'ERP guides, accounting tutorials, business articles, Odoo guides',
            },
        }

        if page_name and page_name in page_meta:
            meta.update(page_meta[page_name])

        meta.update(kwargs)
        return meta


class BlogPost(models.Model):
    _inherit = 'blog.post'

    reading_time = fields.Integer('Reading Time (minutes)', compute='_compute_reading_time', store=True)
    schema_type = fields.Selection([
        ('Article', 'Article'),
        ('BlogPosting', 'Blog Posting'),
        ('TechArticle', 'Technical Article'),
        ('HowTo', 'How-To Guide'),
    ], string='Schema Type', default='Article')

    @api.depends('content')
    def _compute_reading_time(self):
        """Calculate reading time based on word count (200 words/minute)"""
        for post in self:
            if post.content:
                word_count = len(post.content.split())
                post.reading_time = max(1, round(word_count / 200))
            else:
                post.reading_time = 1

    def _get_structured_data(self):
        """Generate JSON-LD structured data for the article"""
        self.ensure_one()
        return {
            "@context": "https://schema.org",
            "@type": self.schema_type or "Article",
            "headline": self.name,
            "description": self.subtitle or (self.teaser[:160] if self.teaser else ''),
            "image": self.env['website'].image_url(self, 'cover_properties') if self.cover_properties else '',
            "datePublished": self.create_date.isoformat() if self.create_date else '',
            "dateModified": self.write_date.isoformat() if self.write_date else '',
            "author": {
                "@type": "Person",
                "name": self.author_id.name if self.author_id else "ChaosHub Team"
            },
            "publisher": {
                "@type": "Organization",
                "name": "ChaosHub.lk",
                "url": "https://chaoshub.lk"
            },
            "wordCount": len(self.content.split()) if self.content else 0,
            "timeRequired": f"PT{self.reading_time}M",
        }
