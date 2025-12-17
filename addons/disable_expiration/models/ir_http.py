# -*- coding: utf-8 -*-
from datetime import datetime, timedelta
from odoo import models


class IrHttp(models.AbstractModel):
    _inherit = 'ir.http'

    def session_info(self):
        """Override session_info to extend expiration date in session"""
        result = super(IrHttp, self).session_info()

        # Set expiration date to far future (50 years)
        future_date = datetime.now() + timedelta(days=365 * 50)
        result['expiration_date'] = future_date.strftime('%Y-%m-%d')
        result['expiration_reason'] = ''

        return result
