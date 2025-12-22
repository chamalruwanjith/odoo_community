# -*- coding: utf-8 -*-
from odoo import models
from werkzeug.urls import url_join, url_encode


class SocialMedia(models.Model):
    _inherit = 'social.media'

    def _add_facebook_accounts_from_iap(self):
        """
        Override to bypass IAP subscription check for Facebook.
        Instead, use direct OAuth if app credentials are configured.
        """
        # Check if Facebook app credentials are configured
        facebook_app_id = self.env['ir.config_parameter'].sudo().get_param('social.facebook_app_id')
        facebook_client_secret = self.env['ir.config_parameter'].sudo().get_param('social.facebook_client_secret')

        if facebook_app_id and facebook_client_secret:
            # Use direct OAuth configuration
            return self._add_facebook_accounts_from_configuration(facebook_app_id)
        else:
            # Return configuration guide instead of error
            return {
                'type': 'ir.actions.client',
                'tag': 'display_notification',
                'params': {
                    'title': 'Social Media Configuration Required',
                    'message': '''
                        To use Social Marketing features, configure your own OAuth apps:

                        1. Go to Settings → Technical → Parameters → System Parameters
                        2. Add these parameters:
                           - social.facebook_app_id: Your Facebook App ID
                           - social.facebook_client_secret: Your Facebook App Secret

                        Get credentials from: https://developers.facebook.com/apps
                    ''',
                    'sticky': False,
                    'type': 'warning',
                }
            }

    def _add_linkedin_accounts_from_iap(self):
        """Override to bypass IAP subscription check for LinkedIn."""
        linkedin_client_id = self.env['ir.config_parameter'].sudo().get_param('social.linkedin_client_id')
        linkedin_client_secret = self.env['ir.config_parameter'].sudo().get_param('social.linkedin_client_secret')

        if linkedin_client_id and linkedin_client_secret:
            return self._add_linkedin_accounts_from_configuration(linkedin_client_id)
        else:
            return {
                'type': 'ir.actions.client',
                'tag': 'display_notification',
                'params': {
                    'title': 'LinkedIn Configuration Required',
                    'message': '''
                        Configure LinkedIn OAuth:

                        1. Go to Settings → Technical → Parameters → System Parameters
                        2. Add:
                           - social.linkedin_client_id
                           - social.linkedin_client_secret

                        Get credentials from: https://www.linkedin.com/developers/apps
                    ''',
                    'sticky': False,
                    'type': 'warning',
                }
            }

    def _add_twitter_accounts_from_iap(self):
        """Override to bypass IAP subscription check for Twitter."""
        twitter_consumer_key = self.env['ir.config_parameter'].sudo().get_param('social.twitter_consumer_key')
        twitter_consumer_secret = self.env['ir.config_parameter'].sudo().get_param('social.twitter_consumer_secret')

        if twitter_consumer_key and twitter_consumer_secret:
            return self._add_twitter_accounts_from_configuration(twitter_consumer_key)
        else:
            return {
                'type': 'ir.actions.client',
                'tag': 'display_notification',
                'params': {
                    'title': 'Twitter Configuration Required',
                    'message': '''
                        Configure Twitter OAuth:

                        1. Go to Settings → Technical → Parameters → System Parameters
                        2. Add:
                           - social.twitter_consumer_key
                           - social.twitter_consumer_secret

                        Get credentials from: https://developer.twitter.com/apps
                    ''',
                    'sticky': False,
                    'type': 'warning',
                }
            }

    def _add_youtube_accounts_from_iap(self):
        """Override to bypass IAP subscription check for YouTube."""
        youtube_client_id = self.env['ir.config_parameter'].sudo().get_param('social.youtube_client_id')
        youtube_client_secret = self.env['ir.config_parameter'].sudo().get_param('social.youtube_client_secret')

        if youtube_client_id and youtube_client_secret:
            return self._add_youtube_accounts_from_configuration(youtube_client_id)
        else:
            return {
                'type': 'ir.actions.client',
                'tag': 'display_notification',
                'params': {
                    'title': 'YouTube Configuration Required',
                    'message': '''
                        Configure YouTube OAuth:

                        1. Go to Settings → Technical → Parameters → System Parameters
                        2. Add:
                           - social.youtube_client_id
                           - social.youtube_client_secret

                        Get credentials from: https://console.cloud.google.com/
                    ''',
                    'sticky': False,
                    'type': 'warning',
                }
            }

    def _add_instagram_accounts_from_iap(self):
        """
        Override to bypass IAP subscription check for Instagram.
        Instagram uses Facebook's API, so use Facebook credentials.
        """
        facebook_app_id = self.env['ir.config_parameter'].sudo().get_param('social.facebook_app_id')
        facebook_client_secret = self.env['ir.config_parameter'].sudo().get_param('social.facebook_client_secret')

        if facebook_app_id and facebook_client_secret:
            return self._add_instagram_accounts_from_configuration(facebook_app_id)
        else:
            return {
                'type': 'ir.actions.client',
                'tag': 'display_notification',
                'params': {
                    'title': 'Instagram Configuration Required',
                    'message': '''
                        Instagram uses Facebook API credentials:

                        1. Go to Settings → Technical → Parameters → System Parameters
                        2. Add:
                           - social.facebook_app_id
                           - social.facebook_client_secret

                        Get credentials from: https://developers.facebook.com/apps
                    ''',
                    'sticky': False,
                    'type': 'warning',
                }
            }
