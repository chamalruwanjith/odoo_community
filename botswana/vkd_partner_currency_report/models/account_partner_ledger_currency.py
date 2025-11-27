# -*- coding: utf-8 -*-

from odoo import models, fields, api, _
from odoo.tools.misc import format_date
from odoo.tools import get_lang, SQL
from odoo.exceptions import UserError

from datetime import timedelta
from collections import defaultdict


class PartnerLedgerCurrencyHandler(models.AbstractModel):
    _name = 'account.partner.ledger.currency.report.handler'
    _inherit = 'account.partner.ledger.report.handler'
    _description = 'Partner Ledger Currency Wise Report Handler'


    def _build_partner_lines(self, report, options, level_shift=0):
        lines = []

        totals_by_column_group = {
            column_group_key: {
                total: 0.0
                for total in ['partner_currency_debit', 'partner_currency_credit', 'amount', 'partner_currency_balance']
            }
            for column_group_key in options['column_groups']
        }

        partners_results = self._query_partners(options)

        search_filter = options.get('filter_search_bar', '')
        accept_unknown_in_filter = search_filter.lower() in self._get_no_partner_line_label().lower()
        for partner, results in partners_results:
            if options['export_mode'] == 'print' and search_filter and not partner and not accept_unknown_in_filter:
                # When printing and searching for a specific partner, make it so we only show its lines, not the 'Unknown Partner' one, that would be
                # shown in case a misc entry with no partner was reconciled with one of the target partner's entries.
                continue

            partner_values = defaultdict(dict)
            for column_group_key in options['column_groups']:
                partner_sum = results.get(column_group_key, {})

                partner_values[column_group_key]['partner_currency_debit'] = partner_sum.get('partner_currency_debit', 0.0)
                partner_values[column_group_key]['partner_currency_credit'] = partner_sum.get('partner_currency_credit', 0.0)
                partner_values[column_group_key]['amount'] = partner_sum.get('amount', 0.0)
                partner_values[column_group_key]['partner_currency_balance'] = partner_sum.get('partner_currency_balance', 0.0)

                totals_by_column_group[column_group_key]['partner_currency_debit'] += partner_values[column_group_key]['partner_currency_debit']
                totals_by_column_group[column_group_key]['partner_currency_credit'] += partner_values[column_group_key]['partner_currency_credit']
                totals_by_column_group[column_group_key]['amount'] += partner_values[column_group_key]['amount']
                totals_by_column_group[column_group_key]['partner_currency_balance'] += partner_values[column_group_key]['partner_currency_balance']

            lines.append(self._get_report_line_partners(options, partner, partner_values, level_shift=level_shift))

        return lines, totals_by_column_group

    def _custom_options_initializer(self, report, options, previous_options):
        super()._custom_options_initializer(report, options, previous_options=previous_options)
        domain = []

        company_ids = report.get_report_company_ids(options)
        exch_code = self.env['res.company'].browse(company_ids).mapped('currency_exchange_journal_id')
        if exch_code:
            domain += ['!', '&', '&', '&', ('partner_currency_credit', '=', 0.0), ('partner_currency_debit', '=', 0.0), ('amount_currency', '!=', 0.0), ('journal_id', 'in', exch_code.ids)]

        if options['export_mode'] == 'print' and options.get('filter_search_bar'):
            domain += [
                '|', ('matched_debit_ids.debit_move_id.partner_id.name', 'ilike', options['filter_search_bar']),
                '|', ('matched_credit_ids.credit_move_id.partner_id.name', 'ilike', options['filter_search_bar']),
                ('partner_id.name', 'ilike', options['filter_search_bar']),
            ]

        options['forced_domain'] = options.get('forced_domain', []) + domain

        if self.env.user.has_group('base.group_multi_currency'):
            options['multi_currency'] = True

        columns_to_hide = []
        options['hide_account'] = (previous_options or {}).get('hide_account', False)
        columns_to_hide += ['journal_code', 'account_code', 'matching_number'] if options['hide_account'] else []

        options['hide_debit_credit'] = (previous_options or {}).get('hide_debit_credit', False)
        columns_to_hide += ['partner_currency_debit', 'partner_currency_credit'] if options['hide_debit_credit'] else ['amount']

        options['columns'] = [col for col in options['columns'] if col['expression_label'] not in columns_to_hide]

        options['buttons'].append({
            'name': _('Send'),
            'action': 'action_send_statements',
            'sequence': 90,
            'always_show': True,
        })

        # Remove duplicate Send buttons
        send_buttons = [btn for btn in options.get('buttons', []) if btn.get('action') == 'action_send_statements']
        if len(send_buttons) > 1:
            # Keep only the first Send button
            options['buttons'] = [btn for btn in options['buttons'] if btn.get('action') != 'action_send_statements']
            options['buttons'].append(send_buttons[0])

    def _query_partners(self, options):
        """ Executes the queries and performs all the computation.
        :return:        A list of tuple (partner, column_group_values) sorted by the table's model _order:
                        - partner is a res.parter record.
                        - column_group_values is a dict(column_group_key, fetched_values), where
                            - column_group_key is a string identifying a column group, like in options['column_groups']
                            - fetched_values is a dictionary containing:
                                - sum:                              {'debit': float, 'credit': float, 'balance': float}
                                - (optional) initial_balance:       {'debit': float, 'credit': float, 'balance': float}
                                - (optional) lines:                 [line_vals_1, line_vals_2, ...]
        """
        def assign_sum(row):
            fields_to_assign = ['partner_currency_balance', 'partner_currency_debit', 'partner_currency_credit', 'amount']
            if any(not company_currency.is_zero(row[field]) for field in fields_to_assign):
                groupby_partners.setdefault(row['groupby'], defaultdict(lambda: defaultdict(float)))
                for field in fields_to_assign:
                    groupby_partners[row['groupby']][row['column_group_key']][field] += row[field]

        company_currency = self.env.company.currency_id

        # Execute the queries and dispatch the results.
        query = self._get_query_sums(options)

        groupby_partners = {}

        self._cr.execute(query)
        for res in self._cr.dictfetchall():
            assign_sum(res)

        # Correct the sums per partner, for the lines without partner reconciled with a line having a partner
        query = self._get_sums_without_partner(options)

        self._cr.execute(query)
        totals = {}
        for total_field in ['partner_currency_debit', 'partner_currency_credit', 'amount', 'partner_currency_balance']:
            totals[total_field] = {col_group_key: 0 for col_group_key in options['column_groups']}

        for row in self._cr.dictfetchall():
            totals['partner_currency_debit'][row['column_group_key']] += row['partner_currency_debit']
            totals['partner_currency_credit'][row['column_group_key']] += row['partner_currency_credit']
            totals['amount'][row['column_group_key']] += row['amount']
            totals['partner_currency_balance'][row['column_group_key']] += row['partner_currency_balance']

            if row['groupby'] not in groupby_partners:
                continue

            assign_sum(row)

        if None in groupby_partners:
            # Debit/credit are inverted for the unknown partner as the computation is made regarding the balance of the known partner
            for column_group_key in options['column_groups']:
                groupby_partners[None][column_group_key]['partner_currency_debit'] += totals['partner_currency_credit'][column_group_key]
                groupby_partners[None][column_group_key]['partner_currency_credit'] += totals['partner_currency_debit'][column_group_key]
                groupby_partners[None][column_group_key]['amount'] += totals['amount'][column_group_key]
                groupby_partners[None][column_group_key]['partner_currency_balance'] -= totals['partner_currency_balance'][column_group_key]

        # Retrieve the partners to browse.
        # groupby_partners.keys() contains all account ids affected by:
        # - the amls in the current period.
        # - the amls affecting the initial balance.
        if groupby_partners:
            # Note a search is done instead of a browse to preserve the table ordering.
            partners = self.env['res.partner'].with_context(active_test=False).search_fetch([('id', 'in', list(groupby_partners.keys()))], ["id", "name", "trust", "company_registry", "vat"])
        else:
            partners = []

        # Add 'Partner Unknown' if needed
        if None in groupby_partners.keys():
            partners = [p for p in partners] + [None]

        return [(partner, groupby_partners[partner.id if partner else None]) for partner in partners]

    def _get_query_sums(self, options) -> SQL:
        """ Construct a query retrieving all the aggregated sums to build the report. It includes:
        - sums for all partners.
        - sums for the initial balances.
        :param options:             The report options.
        :return:                    query as SQL object
        """
        queries = []
        report = self.env.ref('vkd_partner_currency_report.partner_ledger_currency_report')

        # Create the currency table.
        for column_group_key, column_group_options in report._split_options_per_column_group(options).items():
            query = report._get_report_query(column_group_options, 'from_beginning')
            queries.append(SQL(
                """
                SELECT
                    account_move_line.partner_id  AS groupby,
                    %(column_group_key)s          AS column_group_key,
                    SUM(%(debit_select)s)         AS partner_currency_debit,
                    SUM(%(credit_select)s)        AS partner_currency_credit,
                    SUM(%(balance_select)s)       AS amount,
                    SUM(%(balance_select)s)       AS partner_currency_balance
                FROM %(table_references)s
                %(currency_table_join)s
                WHERE %(search_condition)s
                GROUP BY account_move_line.partner_id
                """,
                column_group_key=column_group_key,
                debit_select=report._currency_table_apply_rate(SQL("account_move_line.partner_currency_debit")),
                credit_select=report._currency_table_apply_rate(SQL("account_move_line.partner_currency_credit")),
                balance_select=report._currency_table_apply_rate(SQL("account_move_line.partner_currency_balance")),
                table_references=query.from_clause,
                currency_table_join=report._currency_table_aml_join(column_group_options),
                search_condition=query.where_clause,
            ))

        return SQL(' UNION ALL ').join(queries)

    def _get_initial_balance_values(self, partner_ids, options):
        queries = []
        report = self.env.ref('vkd_partner_currency_report.partner_ledger_currency_report')
        for column_group_key, column_group_options in report._split_options_per_column_group(options).items():
            # Get sums for the initial balance.
            # period: [('date' <= options['date_from'] - 1)]
            new_options = self._get_options_initial_balance(column_group_options)
            query = report._get_report_query(new_options, 'from_beginning', domain=[('partner_id', 'in', partner_ids)])
            queries.append(SQL(
                """
                SELECT
                    account_move_line.partner_id,
                    %(column_group_key)s          AS column_group_key,
                    SUM(%(debit_select)s)         AS partner_currency_debit,
                    SUM(%(credit_select)s)        AS partner_currency_credit,
                    SUM(%(balance_select)s)       AS amount,
                    SUM(%(balance_select)s)       AS partner_currency_balance
                FROM %(table_references)s
                %(currency_table_join)s
                WHERE %(search_condition)s
                GROUP BY account_move_line.partner_id
                """,
                column_group_key=column_group_key,
                debit_select=report._currency_table_apply_rate(SQL("account_move_line.partner_currency_debit")),
                credit_select=report._currency_table_apply_rate(SQL("account_move_line.partner_currency_credit")),
                balance_select=report._currency_table_apply_rate(SQL("account_move_line.partner_currency_balance")),
                table_references=query.from_clause,
                currency_table_join=report._currency_table_aml_join(column_group_options),
                search_condition=query.where_clause,
            ))

        self._cr.execute(SQL(" UNION ALL ").join(queries))

        init_balance_by_col_group = {
            partner_id: {column_group_key: {} for column_group_key in options['column_groups']}
            for partner_id in partner_ids
        }
        for result in self._cr.dictfetchall():
            init_balance_by_col_group[result['partner_id']][result['column_group_key']] = result

        return init_balance_by_col_group

    def _get_sums_without_partner(self, options):
        """ Get the sum of lines without partner reconciled with a line with a partner, grouped by partner. Those lines
        should be considered as belonging to the partner for the reconciled amount as it may clear some of the partner
        invoice/bill and they have to be accounted in the partner balance."""
        queries = []
        report = self.env.ref('vkd_partner_currency_report.partner_ledger_currency_report')
        for column_group_key, column_group_options in report._split_options_per_column_group(options).items():
            query = report._get_report_query(column_group_options, 'from_beginning')
            queries.append(SQL(
                """
                SELECT
                    %(column_group_key)s        AS column_group_key,
                    aml_with_partner.partner_id AS groupby,
                    SUM(%(debit_select)s)       AS partner_currency_debit,
                    SUM(%(credit_select)s)      AS partner_currency_credit,
                    SUM(%(balance_select)s)     AS amount,
                    SUM(%(balance_select)s)     AS partner_currency_balance
                FROM %(table_references)s
                JOIN account_partial_reconcile partial
                    ON account_move_line.id = partial.debit_move_id OR account_move_line.id = partial.credit_move_id
                JOIN account_move_line aml_with_partner ON
                    (aml_with_partner.id = partial.debit_move_id OR aml_with_partner.id = partial.credit_move_id)
                    AND aml_with_partner.partner_id IS NOT NULL
                %(currency_table_join)s
                WHERE partial.max_date <= %(date_to)s AND %(search_condition)s
                    AND account_move_line.partner_id IS NULL
                GROUP BY aml_with_partner.partner_id
                """,
                column_group_key=column_group_key,
                debit_select=report._currency_table_apply_rate(SQL("CASE WHEN aml_with_partner.partner_currency_balance > 0 THEN 0 ELSE partial.amount END")),
                credit_select=report._currency_table_apply_rate(SQL("CASE WHEN aml_with_partner.partner_currency_balance < 0 THEN 0 ELSE partial.amount END")),
                balance_select=report._currency_table_apply_rate(SQL("-SIGN(aml_with_partner.partner_currency_balance) * partial.amount")),
                table_references=query.from_clause,
                currency_table_join=report._currency_table_aml_join(column_group_options, aml_alias=SQL("aml_with_partner")),
                date_to=column_group_options['date']['date_to'],
                search_condition=query.where_clause,
            ))

        return SQL(" UNION ALL ").join(queries)

    def _report_expand_unfoldable_line_partner_ledger(self, line_dict_id, groupby, options, progress, offset, unfold_all_batch_data=None):
        def init_load_more_progress(line_dict):
            return {
                column['column_group_key']: line_col.get('no_format', 0)
                for column, line_col in  zip(options['columns'], line_dict['columns'])
                if column['expression_label'] == 'partner_currency_balance'
            }

        report = self.env.ref('vkd_partner_currency_report.partner_ledger_currency_report')
        markup, model, record_id = report._parse_line_id(line_dict_id)[-1]

        if model != 'res.partner':
            raise UserError(_("Wrong ID for partner ledger line to expand: %s", line_dict_id))

        prefix_groups_count = 0
        for markup, dummy1, dummy2 in report._parse_line_id(line_dict_id):
            if isinstance(markup, dict) and 'groupby_prefix_group' in markup:
                prefix_groups_count += 1
        level_shift = prefix_groups_count * 2

        lines = []

        # Get initial balance
        if offset == 0:
            if unfold_all_batch_data:
                init_balance_by_col_group = unfold_all_batch_data['initial_balances'][record_id]
            else:
                init_balance_by_col_group = self._get_initial_balance_values([record_id], options)[record_id]
            initial_balance_line = report._get_partner_and_general_ledger_initial_balance_line(options, line_dict_id, init_balance_by_col_group, level_shift=level_shift)
            if initial_balance_line:
                lines.append(initial_balance_line)

                # For the first expansion of the line, the initial balance line gives the progress
                progress = init_load_more_progress(initial_balance_line)

        limit_to_load = report.load_more_limit + 1 if report.load_more_limit and options['export_mode'] != 'print' else None

        if unfold_all_batch_data:
            aml_results = unfold_all_batch_data['aml_values'][record_id]
        else:
            aml_results = self._get_aml_values(options, [record_id], offset=offset, limit=limit_to_load)[record_id]

        has_more = False
        treated_results_count = 0
        next_progress = progress
        for result in aml_results:
            if options['export_mode'] != 'print' and report.load_more_limit and treated_results_count == report.load_more_limit:
                # We loaded one more than the limit on purpose: this way we know we need a "load more" line
                has_more = True
                break

            new_line = self._get_report_line_move_line(options, result, line_dict_id, next_progress, level_shift=level_shift)
            lines.append(new_line)
            next_progress = init_load_more_progress(new_line)
            treated_results_count += 1

        return {
            'lines': lines,
            'offset_increment': treated_results_count,
            'has_more': has_more,
            'progress': next_progress
        }

    def _get_report_line_move_line(self, options, aml_query_result, partner_line_id, init_bal_by_col_group,
                                   level_shift=0):
        """
        Override to pass partner currency to move line columns
        """
        if aml_query_result['payment_id']:
            caret_type = 'account.payment'
        else:
            caret_type = 'account.move.line'

        columns = []
        report = self.env['account.report'].browse(options['report_id'])

        # Get partner's currency from partner_line_id
        partner_currency = False
        try:
            markup, model, partner_id = report._parse_line_id(partner_line_id)[-1]
            if model == 'res.partner' and partner_id:
                partner = self.env['res.partner'].browse(partner_id)
                if partner.partner_currency_id:
                    partner_currency = partner.partner_currency_id
        except:
            pass

        for column in options['columns']:
            col_expr_label = column['expression_label']

            if col_expr_label not in aml_query_result:
                raise UserError(_("The column '%s' is not available for this report.", col_expr_label))

            col_value = aml_query_result[col_expr_label] if column['column_group_key'] == aml_query_result[
                'column_group_key'] else None

            if col_value is None:
                columns.append(report._build_column_dict(None, None))
            else:
                currency = False

                if col_expr_label == 'partner_currency_balance':
                    col_value += init_bal_by_col_group[column['column_group_key']]

                # Pass partner currency for partner currency columns
                if col_expr_label in (
                'partner_currency_debit', 'partner_currency_credit', 'partner_currency_balance') and partner_currency:
                    currency = partner_currency
                elif col_expr_label == 'amount_currency':
                    currency = self.env['res.currency'].browse(aml_query_result['currency_id'])
                    if currency == self.env.company.currency_id:
                        col_value = ''

                columns.append(report._build_column_dict(col_value, column, options=options, currency=currency))

        return {
            'id': report._get_generic_line_id('account.move.line', aml_query_result['id'],
                                              parent_line_id=partner_line_id, markup=aml_query_result['partial_id']),
            'parent_id': partner_line_id,
            'name': self._format_aml_name(aml_query_result['name'], aml_query_result['ref'],
                                          aml_query_result['move_name']),
            'columns': columns,
            'caret_options': caret_type,
            'level': 3 + level_shift,
        }

    def _get_report_line_total(self, options, totals_by_column_group):
        """
        Override to show Total in the filtered currency
        When filtering by a specific currency, Total shows in that currency
        """
        column_values = []
        report = self.env['account.report'].browse(options['report_id'])

        # Determine which currency to use for Total
        # If filtering by a specific currency, use that currency
        # Otherwise use company currency
        if options.get('currency_ids') and len(options['currency_ids']) == 1:
            # Single currency filter is active - use that currency
            total_currency = self.env['res.currency'].browse(options['currency_ids'][0])
        else:
            # No filter or multiple currencies - use company currency
            total_currency = self.env.company.currency_id

        for column in options['columns']:
            col_expr_label = column['expression_label']
            col_value = totals_by_column_group[column['column_group_key']].get(col_expr_label)

            # Pass the appropriate currency for partner currency columns in Total line
            if col_expr_label in ('partner_currency_debit', 'partner_currency_credit', 'partner_currency_balance'):
                column_values.append(
                    report._build_column_dict(col_value, column, options=options, currency=total_currency))
            else:
                column_values.append(report._build_column_dict(col_value, column, options=options))

        return {
            'id': report._get_generic_line_id(None, None, markup='total'),
            'name': _('Total'),
            'level': 1,
            'columns': column_values,
        }

    def _get_aml_values(self, options, partner_ids, offset=0, limit=None):
        rslt = {partner_id: [] for partner_id in partner_ids}

        partner_ids_wo_none = [x for x in partner_ids if x]
        directly_linked_aml_partner_clauses = []
        indirectly_linked_aml_partner_clause = SQL('aml_with_partner.partner_id IS NOT NULL')
        if None in partner_ids:
            directly_linked_aml_partner_clauses.append(SQL('account_move_line.partner_id IS NULL'))
        if partner_ids_wo_none:
            directly_linked_aml_partner_clauses.append(SQL('account_move_line.partner_id IN %s', tuple(partner_ids_wo_none)))
            indirectly_linked_aml_partner_clause = SQL('aml_with_partner.partner_id IN %s', tuple(partner_ids_wo_none))
        directly_linked_aml_partner_clause = SQL('(%s)', SQL(' OR ').join(directly_linked_aml_partner_clauses))

        queries = []
        journal_name = self.env['account.journal']._field_to_sql('journal', 'name')
        report = self.env.ref('vkd_partner_currency_report.partner_ledger_currency_report')
        additional_columns = self._get_additional_column_aml_values()
        for column_group_key, group_options in report._split_options_per_column_group(options).items():
            query = report._get_report_query(group_options, 'strict_range')
            account_alias = query.left_join(lhs_alias='account_move_line', lhs_column='account_id', rhs_table='account_account', rhs_column='id', link='account_id')
            account_code = self.env['account.account']._field_to_sql(account_alias, 'code', query)
            account_name = self.env['account.account']._field_to_sql(account_alias, 'name')

            # For the move lines directly linked to this partner
            # ruff: noqa: FURB113
            queries.append(SQL(
                '''
                SELECT
                    account_move_line.id,
                    account_move_line.date_maturity,
                    account_move_line.name,
                    account_move_line.ref,
                    account_move_line.company_id,
                    account_move_line.account_id,
                    account_move_line.payment_id,
                    account_move_line.partner_id,
                    account_move_line.partner_currency_id,
                    account_move_line.amount_currency,
                    account_move_line.matching_number,
                    %(additional_columns)s
                    COALESCE(account_move_line.invoice_date, account_move_line.date) AS invoice_date,
                    %(debit_select)s                                                 AS partner_currency_debit,
                    %(credit_select)s                                                AS partner_currency_credit,
                    %(balance_select)s                                               AS amount,
                    %(balance_select)s                                               AS partner_currency_balance,
                    account_move.name                                                AS move_name,
                    account_move.move_type                                           AS move_type,
                    %(account_code)s                                                 AS account_code,
                    %(account_name)s                                                 AS account_name,
                    journal.code                                                     AS journal_code,
                    %(journal_name)s                                                 AS journal_name,
                    %(column_group_key)s                                             AS column_group_key,
                    'directly_linked_aml'                                            AS key,
                    0                                                                AS partial_id
                FROM %(table_references)s
                JOIN account_move ON account_move.id = account_move_line.move_id
                %(currency_table_join)s
                LEFT JOIN res_company company               ON company.id = account_move_line.company_id
                LEFT JOIN res_partner partner               ON partner.id = account_move_line.partner_id
                LEFT JOIN account_journal journal           ON journal.id = account_move_line.journal_id
                WHERE %(search_condition)s AND %(directly_linked_aml_partner_clause)s
                ORDER BY account_move_line.date, account_move_line.id
                ''',
                additional_columns=additional_columns,
                debit_select=report._currency_table_apply_rate(SQL("account_move_line.partner_currency_debit")),
                credit_select=report._currency_table_apply_rate(SQL("account_move_line.partner_currency_credit")),
                balance_select=report._currency_table_apply_rate(SQL("account_move_line.partner_currency_balance")),
                account_code=account_code,
                account_name=account_name,
                journal_name=journal_name,
                column_group_key=column_group_key,
                table_references=query.from_clause,
                currency_table_join=report._currency_table_aml_join(group_options),
                search_condition=query.where_clause,
                directly_linked_aml_partner_clause=directly_linked_aml_partner_clause,
            ))

            # For the move lines linked to no partner, but reconciled with this partner. They will appear in grey in the report
            queries.append(SQL(
                '''
                SELECT
                    account_move_line.id,
                    account_move_line.date_maturity,
                    account_move_line.name,
                    account_move_line.ref,
                    account_move_line.company_id,
                    account_move_line.account_id,
                    account_move_line.payment_id,
                    aml_with_partner.partner_id,
                    account_move_line.partner_currency_id,
                    account_move_line.amount_currency,
                    account_move_line.matching_number,
                    %(additional_columns)s
                    COALESCE(account_move_line.invoice_date, account_move_line.date) AS invoice_date,
                    %(debit_select)s                                                 AS partner_currency_debit,
                    %(credit_select)s                                                AS partner_currency_credit,
                    %(balance_select)s                                               AS amount,
                    %(balance_select)s                                               AS partner_currency_balance,
                    account_move.name                                                AS move_name,
                    account_move.move_type                                           AS move_type,
                    %(account_code)s                                                 AS account_code,
                    %(account_name)s                                                 AS account_name,
                    journal.code                                                     AS journal_code,
                    %(journal_name)s                                                 AS journal_name,
                    %(column_group_key)s                                             AS column_group_key,
                    'indirectly_linked_aml'                                          AS key,
                    partial.id                                                       AS partial_id
                FROM %(table_references)s
                    %(currency_table_join)s,
                    account_partial_reconcile partial,
                    account_move,
                    account_move_line aml_with_partner,
                    account_journal journal
                WHERE
                    (account_move_line.id = partial.debit_move_id OR account_move_line.id = partial.credit_move_id)
                    AND account_move_line.partner_id IS NULL
                    AND account_move.id = account_move_line.move_id
                    AND (aml_with_partner.id = partial.debit_move_id OR aml_with_partner.id = partial.credit_move_id)
                    AND %(indirectly_linked_aml_partner_clause)s
                    AND journal.id = account_move_line.journal_id
                    AND %(account_alias)s.id = account_move_line.account_id
                    AND %(search_condition)s
                    AND partial.max_date BETWEEN %(date_from)s AND %(date_to)s
                ORDER BY account_move_line.date, account_move_line.id
                ''',
                additional_columns=additional_columns,
                debit_select=report._currency_table_apply_rate(SQL("CASE WHEN aml_with_partner.partner_currency_balance > 0 THEN 0 ELSE partial.amount END")),
                credit_select=report._currency_table_apply_rate(SQL("CASE WHEN aml_with_partner.partner_currency_balance < 0 THEN 0 ELSE partial.amount END")),
                balance_select=report._currency_table_apply_rate(SQL("-SIGN(aml_with_partner.partner_currency_balance) * partial.amount")),
                account_code=account_code,
                account_name=account_name,
                journal_name=journal_name,
                column_group_key=column_group_key,
                table_references=query.from_clause,
                currency_table_join=report._currency_table_aml_join(group_options),
                indirectly_linked_aml_partner_clause=indirectly_linked_aml_partner_clause,
                account_alias=SQL.identifier(account_alias),
                search_condition=query.where_clause,
                date_from=group_options['date']['date_from'],
                date_to=group_options['date']['date_to'],
            ))

        query = SQL(" UNION ALL ").join(SQL("(%s)", query) for query in queries)

        if offset:
            query = SQL('%s OFFSET %s ', query, offset)

        if limit:
            query = SQL('%s LIMIT %s ', query, limit)

        self._cr.execute(query)
        for aml_result in self._cr.dictfetchall():
            if aml_result['key'] == 'indirectly_linked_aml':

                # Append the line to the partner found through the reconciliation.
                if aml_result['partner_id'] in rslt:
                    rslt[aml_result['partner_id']].append(aml_result)

                # Balance it with an additional line in the Unknown Partner section but having reversed amounts.
                if None in rslt:
                    rslt[None].append({
                        **aml_result,
                        'partner_currency_debit': aml_result['partner_currency_credit'],
                        'partner_currency_credit': aml_result['partner_currency_debit'],
                        'amount': aml_result['partner_currency_credit'] - aml_result['partner_currency_debit'],
                        'balance': -aml_result['partner_currency_balance'],
                    })
            else:
                rslt[aml_result['partner_id']].append(aml_result)

        return rslt

    def _get_report_line_partners(self, options, partner, partner_values, level_shift=0):
        company_currency = self.env.company.currency_id

        partner_data = next(iter(partner_values.values()))
        unfoldable = not company_currency.is_zero(
            partner_data.get('partner_currency_debit', 0) or partner_data.get('partner_currency_credit', 0))
        column_values = []
        report = self.env['account.report'].browse(options['report_id'])

        # Get partner's currency for proper currency symbol display
        partner_currency = partner.partner_currency_id if partner and partner.partner_currency_id else False

        for column in options['columns']:
            col_expr_label = column['expression_label']
            value = partner_values[column['column_group_key']].get(col_expr_label)
            unfoldable = unfoldable or (col_expr_label in (
            'partner_currency_debit', 'partner_currency_credit', 'amount') and not company_currency.is_zero(value))

            # Pass currency parameter for partner currency columns to show correct currency symbol
            if col_expr_label in ('partner_currency_debit', 'partner_currency_credit', 'partner_currency_balance'):
                column_values.append(
                    report._build_column_dict(value, column, options=options, currency=partner_currency))
            else:
                column_values.append(report._build_column_dict(value, column, options=options))

        line_id = report._get_generic_line_id('res.partner', partner.id) if partner else report._get_generic_line_id(
            'res.partner', None, markup='no_partner')

        # Add currency symbol to partner name for clarity
        partner_name = partner is not None and (partner.name or '')[:128] or self._get_no_partner_line_label()
        if partner and partner.partner_currency_id:
            partner_name = f"{partner_name} [{partner.partner_currency_id.symbol} - {partner.partner_currency_id.name}]"

        return {
            'id': line_id,
            'name': partner_name,
            'columns': column_values,
            'level': 1 + level_shift,
            'trust': partner.trust if partner else None,
            'unfoldable': unfoldable,
            'unfolded': line_id in options['unfolded_lines'] or options['unfold_all'],
            'expand_function': '_report_expand_unfoldable_line_partner_ledger',
        }
