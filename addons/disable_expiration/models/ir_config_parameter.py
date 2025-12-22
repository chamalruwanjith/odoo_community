# -*- coding: utf-8 -*-
from datetime import datetime, timedelta
from odoo import api, models, SUPERUSER_ID


class IrConfigParameter(models.Model):
    _inherit = 'ir.config_parameter'

    @api.model
    def _auto_extend_expiration(self):
        """
        Automatically extend database expiration date.
        Called by scheduled action.
        """
        IrConfigSudo = self.sudo()

        # Set expiration date to 50 years from now
        future_date = datetime.now() + timedelta(days=365 * 50)
        expiration_str = future_date.strftime('%Y-%m-%d')

        IrConfigSudo.set_param('database.expiration_date', expiration_str)
        IrConfigSudo.set_param('database.expiration_reason', '')

        # Enable social media features by bypassing IAP
        # Set Facebook app credentials to enable direct OAuth (bypasses IAP)
        IrConfigSudo.set_param('social.facebook_use_own_account', True)
        IrConfigSudo.set_param('social.linkedin_use_own_account', True)
        IrConfigSudo.set_param('social.twitter_use_own_account', True)

        # Note: For social media to work, you need to provide your own API keys in:
        # Settings → Technical → Parameters → System Parameters
        # Or configure OAuth apps for each platform

        return True

    @api.model
    def init(self):
        """Extend expiration on module installation"""
        super(IrConfigParameter, self).init()
        # Run on module install/update
        if self.env.uid == SUPERUSER_ID:
            self._auto_extend_expiration()
