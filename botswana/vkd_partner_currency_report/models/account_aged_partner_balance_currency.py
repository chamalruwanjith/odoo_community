# -*- coding: utf-8 -*-

from odoo import models, fields, _
from odoo.tools import SQL

from dateutil.relativedelta import relativedelta
from itertools import chain


class AgedPartnerBalanceCurrencyHandler(models.AbstractModel):
    _name = 'account.aged.partner.balance.currency.report.handler'
    _inherit = ['account.aged.partner.balance.report.handler', 'account.report.custom.handler']
    _description = 'Aged Partner Balance Currency Wise Report Handler'


    def _aged_partner_report_custom_engine_common(self, options, internal_type, current_groupby, next_groupby, offset=0,
                                                  limit=None):

        report = self.env['account.report'].browse(options['report_id'])
        report._check_groupby_fields(
            (next_groupby.split(',') if next_groupby else []) + ([current_groupby] if current_groupby else []))

        def minus_days(date_obj, days):
            return fields.Date.to_string(date_obj - relativedelta(days=days))

        aging_date_field = SQL.identifier('invoice_date') if options['aging_based_on'] == 'base_on_invoice_date' else SQL.identifier(
            'date_maturity')
        date_to = fields.Date.from_string(options['date']['date_to'])
        interval = options['aging_interval']
        periods = [(False, fields.Date.to_string(date_to))]
        # Since we added the first period in the list we have to do one less iteration
        nb_periods = len(
            [column for column in options['columns'] if column['expression_label'].startswith('period')]) - 1
        for i in range(nb_periods):
            start_date = minus_days(date_to, (interval * i) + 1)
            # The last element of the list will have False for the end date
            end_date = minus_days(date_to, interval * (i + 1)) if i < nb_periods - 1 else False
            periods.append((start_date, end_date))

        def build_result_dict(report, query_res_lines):
            rslt = {f'period{i}': 0 for i in range(len(periods))}

            for query_res in query_res_lines:
                for i in range(len(periods)):
                    period_key = f'period{i}'
                    rslt[period_key] += query_res[period_key]

            if current_groupby == 'id':
                query_res = query_res_lines[
                    0]  # We're grouping by id, so there is only 1 element in query_res_lines anyway
                currency = self.env['res.currency'].browse(query_res['currency_id'][0]) if len(
                    query_res['currency_id']) == 1 else None

                # Get partner's currency for detail lines
                partner_id = query_res['partner_id'][0] if query_res['partner_id'] else None
                partner_currency_id = None

                if partner_id:
                    partner = self.env['res.partner'].browse(partner_id)
                    if partner.partner_currency_id:
                        partner_currency_id = partner.partner_currency_id.id

                # If no partner currency and filter is active, use filtered currency
                if not partner_currency_id and options.get('currency_ids') and len(options['currency_ids']) == 1:
                    partner_currency_id = options['currency_ids'][0]

                # If still no currency, use the invoice currency
                if not partner_currency_id:
                    partner_currency_id = query_res['currency_id'][0] if len(query_res['currency_id']) == 1 else None

                rslt.update({
                    'invoice_date': query_res['invoice_date'][0] if len(query_res['invoice_date']) == 1 else None,
                    'due_date': query_res['due_date'][0] if len(query_res['due_date']) == 1 else None,
                    'amount_currency': query_res['amount_currency'],
                    'currency_id': partner_currency_id,
                    'currency': currency.display_name if currency else None,
                    'account_name': query_res['account_name'][0] if len(query_res['account_name']) == 1 else None,
                    'total': None,
                    'has_sublines': query_res['aml_count'] > 0,

                    # Needed by the custom_unfold_all_batch_data_generator, to speed-up unfold_all
                    'partner_id': query_res['partner_id'][0] if query_res['partner_id'] else None,
                })
            else:
                # For partner groupby, get the partner and its currency
                partner_id = query_res_lines[0].get('grouping_key') if query_res_lines else None
                partner_currency_id = None

                if partner_id and current_groupby == 'partner_id':
                    partner = self.env['res.partner'].browse(partner_id)
                    if partner.partner_currency_id:
                        partner_currency_id = partner.partner_currency_id.id

                # If single currency filter is active and no partner_currency_id, use filtered currency
                if not partner_currency_id and options.get('currency_ids') and len(options['currency_ids']) == 1:
                    partner_currency_id = options['currency_ids'][0]

                rslt.update({
                    'invoice_date': None,
                    'due_date': None,
                    'amount_currency': None,
                    'currency_id': partner_currency_id,  # Return currency_id for the framework
                    'currency': None,
                    'account_name': None,
                    'total': sum(rslt[f'period{i}'] for i in range(len(periods))),
                    'has_sublines': False,
                })

            return rslt

        # Build period table
        period_table_format = ('(VALUES %s)' % ','.join("(%s, %s, %s)" for period in periods))
        params = list(chain.from_iterable(
            (period[0] or None, period[1] or None, i)
            for i, period in enumerate(periods)
        ))
        period_table = SQL(period_table_format, *params)

        # Build query
        query = report._get_report_query(options, 'strict_range',
                                         domain=[('account_id.account_type', '=', internal_type)])
        account_alias = query.left_join(lhs_alias='account_move_line', lhs_column='account_id',
                                        rhs_table='account_account', rhs_column='id', link='account_id')
        account_code = self.env['account.account']._field_to_sql(account_alias, 'code', query)

        always_present_groupby = SQL("period_table.period_index")
        if current_groupby:
            select_from_groupby = SQL("%s AS grouping_key,", SQL.identifier("account_move_line", current_groupby))
            groupby_clause = SQL("%s, %s", SQL.identifier("account_move_line", current_groupby), always_present_groupby)
        else:
            select_from_groupby = SQL()
            groupby_clause = always_present_groupby
        multiplicator = -1 if internal_type == 'liability_payable' else 1
        select_period_query = SQL(',').join(
            SQL("""
                CASE WHEN period_table.period_index = %(period_index)s
                THEN %(multiplicator)s * SUM(%(balance_select)s)
                ELSE 0 END AS %(column_name)s
                """,
                period_index=i,
                multiplicator=multiplicator,
                column_name=SQL.identifier(f"period{i}"),
                balance_select=report._currency_table_apply_rate(SQL(
                    "account_move_line.partner_currency_balance - COALESCE(part_debit.amount, 0) + COALESCE(part_credit.amount, 0)"
                )),
                )
            for i in range(len(periods))
        )

        tail_query = report._get_engine_query_tail(offset, limit)
        query = SQL(
            """
            WITH period_table(date_start, date_stop, period_index) AS (%(period_table)s)

            SELECT
                %(select_from_groupby)s
                %(multiplicator)s * (
                    SUM(account_move_line.amount_currency)
                    - COALESCE(SUM(part_debit.debit_amount_currency), 0)
                    + COALESCE(SUM(part_credit.credit_amount_currency), 0)
                ) AS amount_currency,
                ARRAY_AGG(DISTINCT account_move_line.partner_id) AS partner_id,
                ARRAY_AGG(DISTINCT account_move_line.%(aging_date_field)s) AS invoice_date,
                ARRAY_AGG(DISTINCT account_move_line.date_maturity) AS due_date,
                ARRAY_AGG(DISTINCT account_move_line.currency_id) AS currency_id,
                ARRAY_AGG(DISTINCT %(account_code)s) AS account_name,
                COUNT(account_move_line.id) AS aml_count,
                %(select_period_query)s

            FROM %(table_references)s
            %(currency_table_join)s

            LEFT JOIN LATERAL (
                SELECT
                    SUM(part.amount) AS amount,
                    SUM(part.debit_amount_currency) AS debit_amount_currency,
                    part.debit_move_id
                FROM account_partial_reconcile part
                WHERE part.max_date <= %(date_to)s AND part.debit_move_id = account_move_line.id
                GROUP BY part.debit_move_id
            ) part_debit ON TRUE

            LEFT JOIN LATERAL (
                SELECT
                    SUM(part.amount) AS amount,
                    SUM(part.credit_amount_currency) AS credit_amount_currency,
                    part.credit_move_id
                FROM account_partial_reconcile part
                WHERE part.max_date <= %(date_to)s AND part.credit_move_id = account_move_line.id
                GROUP BY part.credit_move_id
            ) part_credit ON TRUE

            JOIN period_table ON
                (
                    period_table.date_start IS NULL
                    OR COALESCE(account_move_line.%(aging_date_field)s, account_move_line.date) <= DATE(period_table.date_start)
                )
                AND
                (
                    period_table.date_stop IS NULL
                    OR COALESCE(account_move_line.%(aging_date_field)s, account_move_line.date) >= DATE(period_table.date_stop)
                )

            WHERE %(search_condition)s

            GROUP BY %(groupby_clause)s

            HAVING
                ROUND(SUM(%(having_debit)s), %(currency_precision)s) != 0
                OR ROUND(SUM(%(having_credit)s), %(currency_precision)s) != 0
            %(tail_query)s
            """,
            account_code=account_code,
            period_table=period_table,
            select_from_groupby=select_from_groupby,
            select_period_query=select_period_query,
            multiplicator=multiplicator,
            aging_date_field=aging_date_field,
            table_references=query.from_clause,
            currency_table_join=report._currency_table_aml_join(options),
            date_to=date_to,
            search_condition=query.where_clause,
            groupby_clause=groupby_clause,
            having_debit=report._currency_table_apply_rate(
                SQL("CASE WHEN account_move_line.partner_currency_balance > 0  THEN account_move_line.partner_currency_balance else 0 END - COALESCE(part_debit.amount, 0)")),
            having_credit=report._currency_table_apply_rate(
                SQL("CASE WHEN account_move_line.partner_currency_balance < 0  THEN -account_move_line.partner_currency_balance else 0 END - COALESCE(part_credit.amount, 0)")),
            currency_precision=self.env.company.currency_id.decimal_places,
            tail_query=tail_query,
        )

        self._cr.execute(query)
        query_res_lines = self._cr.dictfetchall()

        if not current_groupby:
            return build_result_dict(report, query_res_lines)
        else:
            rslt = []

            all_res_per_grouping_key = {}
            for query_res in query_res_lines:
                grouping_key = query_res['grouping_key']
                all_res_per_grouping_key.setdefault(grouping_key, []).append(query_res)

            for grouping_key, query_res_lines in all_res_per_grouping_key.items():
                rslt.append((grouping_key, build_result_dict(report, query_res_lines)))

            return rslt


class AgedReceivableCurrencyHandler(models.AbstractModel):
    _name = 'account.aged.receivable.currency.report.handler'
    _inherit = 'account.aged.receivable.report.handler'
    _description = 'Aged Receivable Currency Custom Handler'

    def _report_custom_engine_aged_receivable(self, expressions, options, date_scope, current_groupby, next_groupby,
                                              offset=0, limit=None, warnings=None):
        handler = self.env['account.aged.partner.balance.currency.report.handler']
        return handler._aged_partner_report_custom_engine_common(
            options,
            'asset_receivable',
            current_groupby,
            next_groupby,
            offset=offset,
            limit=limit
        )


class AgedPayableCurrencyHandler(models.AbstractModel):
    _name = 'account.aged.payable.currency.report.handler'
    _inherit = 'account.aged.payable.report.handler'
    _description = 'Aged Payable Currency Custom Handler'

    def _report_custom_engine_aged_payable(self, expressions, options, date_scope, current_groupby, next_groupby,
                                           offset=0, limit=None, warnings=None):
        handler = self.env['account.aged.partner.balance.currency.report.handler']
        return handler._aged_partner_report_custom_engine_common(
            options,
            'liability_payable',
            current_groupby,
            next_groupby,
            offset=offset,
            limit=limit
        )