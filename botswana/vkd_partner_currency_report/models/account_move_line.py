# -*- coding: utf-8 -*-

from odoo import models, fields, api


class AccountMoveLine(models.Model):
    _inherit = 'account.move.line'

    partner_currency_id = fields.Many2one(
        'res.currency',
        string='Partner Currency',
        related='partner_id.partner_currency_id',
        store=True,
        readonly=True,
    )

    partner_currency_balance = fields.Monetary(
        string='Partner Currency Balance',
        currency_field='partner_currency_id',
        compute='_compute_partner_currency_balance',
        store=True,
        readonly=False,
    )

    partner_currency_debit = fields.Monetary(
        string='Partner Currency Debit',
        currency_field='partner_currency_id',
        compute='_compute_partner_currency_debit_credit',
        inverse='_inverse_partner_currency_debit',
        store=True,
    )

    partner_currency_credit = fields.Monetary(
        string='Partner Currency Credit',
        currency_field='partner_currency_id',
        compute='_compute_partner_currency_debit_credit',
        inverse='_inverse_partner_currency_credit',
        store=True,
    )

    @api.depends('balance', 'partner_id.partner_currency_id', 'company_currency_id',
                 'date', 'move_id.invoice_date')
    def _compute_partner_currency_balance(self):
        for line in self:
            if line.display_type in ('line_section', 'line_note'):
                line.partner_currency_balance = False
                continue

            if not line.partner_id or not line.partner_id.partner_currency_id:
                line.partner_currency_balance = 0.0
                continue

            partner_currency = line.partner_id.partner_currency_id
            company_currency = line.company_currency_id

            if company_currency == partner_currency:
                line.partner_currency_balance = line.balance
                continue

            conversion_date = line.move_id.invoice_date or line.move_id.date or fields.Date.context_today(self)

            if line.balance:
                line.partner_currency_balance = company_currency._convert(
                    line.balance,
                    partner_currency,
                    line.company_id,
                    conversion_date
                )
            else:
                line.partner_currency_balance = 0.0

    @api.depends('partner_currency_balance', 'move_id.is_storno')
    def _compute_partner_currency_debit_credit(self):
        for line in self:
            if not line.is_storno:
                line.partner_currency_debit = line.partner_currency_balance if line.partner_currency_balance > 0.0 else 0.0
                line.partner_currency_credit = -line.partner_currency_balance if line.partner_currency_balance < 0.0 else 0.0
            else:
                line.partner_currency_debit = line.partner_currency_balance if line.partner_currency_balance < 0.0 else 0.0
                line.partner_currency_credit = -line.partner_currency_balance if line.partner_currency_balance > 0.0 else 0.0

    def _inverse_partner_currency_debit(self):
        for line in self:
            if line.partner_currency_debit:
                line.partner_currency_credit = 0
            line.partner_currency_balance = line.partner_currency_debit - line.partner_currency_credit

    def _inverse_partner_currency_credit(self):
        for line in self:
            if line.partner_currency_credit:
                line.partner_currency_debit = 0
            line.partner_currency_balance = line.partner_currency_debit - line.partner_currency_credit