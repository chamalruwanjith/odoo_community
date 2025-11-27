# -*- coding: utf-8 -*-

from odoo import api, models, fields, _


class AccountReport(models.Model):
    _inherit = 'account.report'

    filter_currency = fields.Boolean(
        string="Currency",
        help="Enable currency-based filtering for this report",
        compute=lambda x: x._compute_report_option_filter('filter_currency'),
        readonly=False,
        store=True,
        depends=['root_report_id', 'section_main_report_ids'],
    )

    def _init_options_currency(self, options, previous_options):
        if not self.filter_currency:
            return

        options['currency_filter'] = True
        previous_currency_ids = previous_options.get('currency_ids') or []

        selected_currency_ids = [int(currency) for currency in previous_currency_ids]
        selected_currencies = selected_currency_ids and self.env['res.currency'].with_context(active_test=False).search(
            [('id', 'in', selected_currency_ids)]) or self.env['res.currency']
        options['selected_currency_names'] = selected_currencies.mapped('name')
        options['currency_ids'] = selected_currencies.ids

    @api.model
    def _get_options_currency_domain(self, options):
        domain = []
        if options.get('currency_ids'):
            currency_ids = [int(currency) for currency in options['currency_ids']]
            domain.append(('partner_id.partner_currency_id', 'in', currency_ids))
        return domain

    def _get_options_domain(self, options, date_scope):
        self.ensure_one()
        domain = super()._get_options_domain(options, date_scope)
        domain += self._get_options_currency_domain(options)
        return domain


    def _get_partner_and_general_ledger_initial_balance_line(self, options, parent_line_id, eval_dict,
                                                             account_currency=None, level_shift=0):
        """
        pass partner currency for initial balance line
        """
        line_columns = []
        report = self.env['account.report'].browse(options['report_id'])

        # Get partner currency from parent_line_id
        partner_currency = None
        try:
            markup, model, partner_id = report._parse_line_id(parent_line_id)[-1]
            if model == 'res.partner' and partner_id:
                partner = self.env['res.partner'].browse(partner_id)
                if partner.partner_currency_id:
                    partner_currency = partner.partner_currency_id
        except:
            pass

        for column in options['columns']:
            col_value = eval_dict[column['column_group_key']].get(column['expression_label'])
            col_expr_label = column['expression_label']

            if col_value is None or (col_expr_label == 'amount_currency' and not account_currency):
                line_columns.append(report._build_column_dict(None, None))
            else:
                # Determine which currency to use
                currency = None
                if col_expr_label == 'amount_currency':
                    currency = account_currency
                elif col_expr_label in (
                'partner_currency_debit', 'partner_currency_credit', 'partner_currency_balance') and partner_currency:
                    currency = partner_currency

                line_columns.append(report._build_column_dict(
                    col_value,
                    column,
                    options=options,
                    currency=currency,
                ))

        # Display unfold & initial balance even when debit/credit column is hidden and the balance == 0
        if not any(isinstance(column.get('no_format'), (int, float)) and column.get('expression_label') not in (
        'balance', 'partner_currency_balance') for column in line_columns):
            return None

        return {
            'id': report._get_generic_line_id(None, None, parent_line_id=parent_line_id, markup='initial'),
            'name': _("Initial Balance"),
            'level': 3 + level_shift,
            'parent_id': parent_line_id,
            'columns': line_columns,
        }