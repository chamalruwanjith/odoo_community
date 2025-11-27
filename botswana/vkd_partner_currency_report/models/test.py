
from odoo import models, fields, api
from odoo.tools.misc import formatLang


class PartnerLedgerCurrencyHandler(models.AbstractModel):
    _name = 'account.partner.ledger.currency.report.handler'
    _inherit = 'account.partner.ledger.report.handler'
    _description = 'Partner Ledger Currency Wise Report Handler'

    def _custom_options_initializer(self, report, options, previous_options):
        """Initialize custom options including currency filter"""
        super()._custom_options_initializer(report, options, previous_options=previous_options)

        # Add account type domain filter for receivable and payable
        account_type_domain = [('account_id.account_type', 'in', ['asset_receivable', 'liability_payable'])]
        options['forced_domain'] = options.get('forced_domain', []) + account_type_domain

        # Initialize currency filter
        if hasattr(report, 'filter_currency') and report.filter_currency:
            report._init_options_currency(options, previous_options)

    def _dynamic_lines_generator(self, report, options, all_column_groups_expression_totals, warnings=None):
        """Generate lines filtered by selected currency and show amounts in partner currency"""

        # Generate lines (domain already applied via _get_options_domain)
        lines = super()._dynamic_lines_generator(report, options, all_column_groups_expression_totals, warnings)

        # If single currency selected, convert amounts to that currency
        if options.get('currency_ids') and len(options['currency_ids']) == 1:
            lines = self._convert_lines_to_partner_currency(lines, options)
            lines = self._recalculate_total_line(lines, options)

        return lines

    def _recalculate_total_line(self, lines, options):
        """
        Recalculate the Total line by summing only partner lines with the selected currency
        """
        target_currency = self.env['res.currency'].browse(options['currency_ids'][0])

        # Find the Total line (should be the last line)
        total_line_index = None
        for i, line_tuple in enumerate(lines):
            if isinstance(line_tuple, tuple) and len(line_tuple) >= 2:
                line = line_tuple[1]
                if line.get('name') == 'Total':
                    total_line_index = i
                    break

        if total_line_index is None:
            return lines

        # Calculate new totals by summing partner lines with target currency
        new_totals = {}
        for col_index, column in enumerate(options['columns']):
            col_expr_label = column['expression_label']
            col_group_key = column['column_group_key']

            if col_group_key not in new_totals:
                new_totals[col_group_key] = {'debit': 0.0, 'credit': 0.0, 'balance': 0.0, 'amount': 0.0}

            # Sum up amounts from partner lines with the target currency
            for line_tuple in lines:
                if isinstance(line_tuple, tuple) and len(line_tuple) >= 2:
                    line = line_tuple[1]

                    # Only sum partner lines (level 1) with the target currency
                    if line.get('level') == 1 and line.get('partner_currency_id') == target_currency.id:
                        if col_index < len(line.get('columns', [])):
                            col = line['columns'][col_index]
                            if col.get('no_format') is not None and col_expr_label in (
                            'debit', 'credit', 'balance', 'amount'):
                                value = col.get('no_format', 0.0)
                                if isinstance(value, (int, float)):
                                    new_totals[col_group_key][col_expr_label] += value

        # Update the Total line with new calculated values
        total_line_tuple = lines[total_line_index]
        if isinstance(total_line_tuple, tuple) and len(total_line_tuple) >= 2:
            total_line = total_line_tuple[1]

            for col_index, column in enumerate(options['columns']):
                col_expr_label = column['expression_label']
                col_group_key = column['column_group_key']

                if col_index < len(total_line.get('columns', [])):
                    col = total_line['columns'][col_index]

                    if col_expr_label in new_totals.get(col_group_key, {}):
                        new_value = new_totals[col_group_key][col_expr_label]
                        col['no_format'] = new_value

                        # Update the formatted name using formatLang directly
                        if col.get('figure_type') == 'monetary':
                            col['name'] = formatLang(
                                self.env,
                                new_value,
                                currency_obj=target_currency
                            )

        return lines


    def _convert_lines_to_partner_currency(self, lines, options):
        """
        Convert all monetary amounts to the selected partner currency.
        This shows Customer A (LKR) with all amounts in LKR, not USD.
        """
        target_currency = self.env['res.currency'].browse(options['currency_ids'][0])
        company_currency = self.env.company.currency_id

        # If currencies are the same, no conversion needed
        if company_currency == target_currency:
            return lines

        for line_tuple in lines:
            if not line_tuple or not isinstance(line_tuple, tuple) or len(line_tuple) < 2:
                continue

            # Line structure is (index, line_dict)
            line = line_tuple[1]

            if not line or not isinstance(line, dict):
                continue

            # Check if this is the main Total line (no partner_currency_id)
            if line.get('name') == 'Total' and 'partner_currency_id' not in line:
                # This is the grand total - skip it for now, will be recalculated
                continue

            # Check if this line has partner currency info (it's a partner line)
            if 'partner_currency_id' in line and line.get('partner_currency_id'):
                partner_currency_id = line['partner_currency_id']

                # Only convert if partner currency matches the selected currency
                if partner_currency_id == target_currency.id:
                    # Convert amounts in columns
                    for col in line.get('columns', []):
                        # Check if this is a monetary column with a value
                        if col.get('figure_type') == 'monetary' and col.get('no_format') is not None:
                            amount_company_currency = col.get('no_format', 0.0)

                            # Skip if amount is zero or string
                            if not amount_company_currency or isinstance(amount_company_currency, str):
                                continue

                            # Convert from company currency to partner currency
                            amount_partner_currency = company_currency._convert(
                                amount_company_currency,
                                target_currency,
                                self.env.company,
                                fields.Date.today()
                            )

                            # Update the column values
                            col['no_format'] = amount_partner_currency

                            # Update formatted value
                            if 'name' in col:
                                col['name'] = self.env['account.report'].format_value(
                                    amount_partner_currency,
                                    currency=target_currency,
                                    figure_type='monetary'
                                )

        return lines

    def _get_report_line_move_line(self, options, aml_query_result, partner_line_id, init_bal_by_col_group,
                                   level_shift=0):
        """
        Override to convert amounts to partner currency for journal entry lines
        """
        # Get the line from parent method
        line_dict = super()._get_report_line_move_line(options, aml_query_result, partner_line_id,
                                                       init_bal_by_col_group, level_shift)

        # If single currency selected, convert amounts to that currency
        if options.get('currency_ids') and len(options['currency_ids']) == 1:
            target_currency = self.env['res.currency'].browse(options['currency_ids'][0])
            company_currency = self.env.company.currency_id

            if company_currency != target_currency:
                # Get partner from parent_line_id to check if conversion is needed
                try:
                    model, partner_id = self.env['account.report']._get_model_info_from_id(partner_line_id)
                    if model == 'res.partner' and partner_id:
                        partner = self.env['res.partner'].browse(partner_id)

                        # Only convert if partner has the target currency
                        if partner.partner_currency_id and partner.partner_currency_id.id == target_currency.id:
                            # Track the initial balance for correct cumulative balance calculation
                            converted_init_balance = {}

                            # First, convert initial balances
                            for col_group_key, init_bal in init_bal_by_col_group.items():
                                if init_bal:
                                    converted_init_balance[col_group_key] = company_currency._convert(
                                        init_bal,
                                        target_currency,
                                        self.env.company,
                                        fields.Date.today()
                                    )
                                else:
                                    converted_init_balance[col_group_key] = 0.0

                            # Convert amounts in columns
                            for i, col in enumerate(line_dict.get('columns', [])):
                                col_expr_label = options['columns'][i].get('expression_label')
                                col_group_key = options['columns'][i].get('column_group_key')

                                # Convert monetary columns (debit, credit, balance)
                                if col_expr_label in ('debit', 'credit', 'balance', 'amount') and col.get(
                                        'no_format') is not None:
                                    amount_company_currency = col.get('no_format', 0.0)

                                    # Skip if it's a string (empty value)
                                    if isinstance(amount_company_currency, str):
                                        continue

                                    if col_expr_label == 'balance':
                                        # Balance includes init_bal, so we need to subtract it, convert, then add back converted init_bal
                                        init_bal = init_bal_by_col_group.get(col_group_key, 0.0)
                                        amount_without_init = amount_company_currency - init_bal

                                        # Convert the amount without initial balance
                                        converted_amount = company_currency._convert(
                                            amount_without_init,
                                            target_currency,
                                            self.env.company,
                                            fields.Date.today()
                                        )

                                        # Add back the converted initial balance
                                        amount_partner_currency = converted_amount + converted_init_balance.get(
                                            col_group_key, 0.0)
                                    else:
                                        # For debit, credit, amount - just convert
                                        amount_partner_currency = company_currency._convert(
                                            amount_company_currency,
                                            target_currency,
                                            self.env.company,
                                            fields.Date.today()
                                        )

                                    col['no_format'] = amount_partner_currency

                                    # Update formatted value
                                    if 'name' in col:
                                        col['name'] = self.env['account.report'].format_value(
                                            amount_partner_currency,
                                            currency=target_currency,
                                            figure_type='monetary'
                                        )
                except Exception:
                    # If we can't get the partner, just return the line as-is
                    pass

        return line_dict

    def _report_expand_unfoldable_line_partner_ledger(self, line_dict_id, groupby, options, progress, offset,
                                                      unfold_all_batch_data=None):
        """
        Override to convert initial balance and total lines to partner currency
        """
        result = super()._report_expand_unfoldable_line_partner_ledger(line_dict_id, groupby, options, progress, offset,
                                                                       unfold_all_batch_data)

        # If single currency selected, convert the initial balance line and total line
        if options.get('currency_ids') and len(options['currency_ids']) == 1:
            target_currency = self.env['res.currency'].browse(options['currency_ids'][0])
            company_currency = self.env.company.currency_id

            if company_currency != target_currency and 'lines' in result:
                # Get partner from line_dict_id
                try:
                    markup, model, partner_id = self.env['account.report']._parse_line_id(line_dict_id)[-1]
                    if model == 'res.partner' and partner_id:
                        partner = self.env['res.partner'].browse(partner_id)

                        # Only convert if partner has the target currency
                        if partner.partner_currency_id and partner.partner_currency_id.id == target_currency.id:
                            # Convert all lines (initial balance, amls, total)
                            for line_tuple in result['lines']:
                                if isinstance(line_tuple, tuple) and len(line_tuple) >= 2:
                                    line = line_tuple[1]

                                    # Convert columns
                                    for col in line.get('columns', []):
                                        if col.get('figure_type') == 'monetary' and col.get('no_format') is not None:
                                            amount_company_currency = col.get('no_format', 0.0)

                                            if isinstance(amount_company_currency,
                                                          (int, float)) and amount_company_currency != 0:
                                                amount_partner_currency = company_currency._convert(
                                                    amount_company_currency,
                                                    target_currency,
                                                    self.env.company,
                                                    fields.Date.today()
                                                )

                                                col['no_format'] = amount_partner_currency

                                                if 'name' in col:
                                                    col['name'] = self.env['account.report'].format_value(
                                                        amount_partner_currency,
                                                        currency=target_currency,
                                                        figure_type='monetary'
                                                    )
                except Exception:
                    pass

        return result

    def _get_report_line_partners(self, options, partner, partner_values, level_shift=0):
        """
        Override to show currency info and ensure amounts are in partner currency
        """
        line_dict = super()._get_report_line_partners(options, partner, partner_values, level_shift)

        # Add currency information to line if partner has currency
        if partner and partner.partner_currency_id:
            line_dict['partner_currency_id'] = partner.partner_currency_id.id
            line_dict['partner_currency_code'] = partner.partner_currency_id.name

            # Add currency indicator to partner name
            currency_code = partner.partner_currency_id.name
            line_dict['name'] = f"{line_dict['name']} [{currency_code}]"

        return line_dict