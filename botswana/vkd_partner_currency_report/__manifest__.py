# -*- coding: utf-8 -*-
{
    'name': 'Partner Currency Reports',
    'version': '18.0.1.0.0',
    'category': 'Accounting/Accounting',
    'summary': 'Currency-wise Partner Reports - Show amounts in Partner Currency',
    'description': """
        Currency-Wise Accounting Reports
            Add currency field to partners
            Filter reports by partner's assigned currency
            All amounts shown in PARTNER CURRENCY, not company currency
        
        Customer A - Partner Currency: LKR
          - Invoice in AED → Converted and shown in LKR
          - Payment in AUD → Converted and shown in LKR
          - Report shows: All amounts in LKR
        
        Customer B - Partner Currency: AUD  
          - Invoice in USD → Converted and shown in AUD
          - Payment in LKR → Converted and shown in AUD
          - Report shows: All amounts in AUD
        
        When you select "LKR" in the currency filter:
        → Shows only partners with partner currency = LKR
        → All their transactions displayed in LKR amounts
        
        This module extends the standard Odoo accounting reports to provide
        currency-wise filtering and reporting with amounts in partner currency.
              
    """,
    'author': 'VK DATA ApS',
    'website': 'https://vkdata.dk',
    'license': 'OPL-1',
    'depends': [
        'account',
        'account_reports',
    ],
    'data': [
        'security/ir.model.access.csv',
        'views/res_partner_views.xml',
        'data/partner_ledger_currency_report.xml',
        'data/aged_partner_balance_currency_report.xml',
        'views/report_menus.xml',
        'views/account_report_view.xml',
    ],
    'assets': {
        'web.assets_backend': [
            'vkd_partner_currency_report/static/src/components/currency_filter/currency_filter.xml',
            'vkd_partner_currency_report/static/src/components/currency_filter/currency_filter_dropdown.xml',
        ],
    },
    'installable': True,
    'application': False,
    'auto_install': False,
}
