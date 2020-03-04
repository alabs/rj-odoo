# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import fields, models, tools


class ReportAccountReport(models.Model):
    _name = "report.account.income.viz"
    _description = "Account Income Stage"
    _order = 'name desc'
    _auto = False

    name = fields.Char(string='Project Title', readonly=True)
    nbr = fields.Integer('# of Tasks', readonly=True)
    income = fields.Float('Expense', readonly=True)
    expense = fields.Float('Income', readonly=True)
    expense_income = fields.Float('Expense/Income', readonly=True,compute="compute_expense_income",store=True)
    from_where_the_value_comming = fields.Char('Expense/Income')
    date_time = fields.Datetime('Intervals')
    company_id = fields.Many2one('res.company', string='Company', required=True,
                                 default=lambda self: self.env.user.company_id)

    def compute_expense_income(self):
        for i in self.env['account.move.line'].search([]):
            if(i.credit != 0):
                self.expense_income = i.credit
            elif i.debit != 0:
                self.expense_income = i.debit
        print('comp')

    def _select(self):
        select_str = """
             SELECT
                    (select 1 ) AS nbr, account_id as account_id, account_move_line.account_id as id, 
                        COALESCE(SUM(debit),0) - COALESCE(SUM(credit), 0) as balance,account_move_line.create_date as date_time,
                        greatest(COALESCE(SUM(debit), 0), COALESCE(SUM(credit), 0)) AS expense_income,

                        CASE WHEN COALESCE(SUM(debit) > COALESCE(SUM(credit), 0)) THEN 'expense'
                        ELSE 'income' END AS from_where_the_value_comming,

                        COALESCE(SUM(debit), 0) as income , COALESCE(SUM(credit), 0) as expense
                    

        """
        return select_str

    def _group_by(self):
        group_by_str = """
                GROUP BY
                    account_id,account_move_line.account_id,account_move_line.create_date
        """
        return group_by_str

    def init(self):
        tools.drop_view_if_exists(self._cr, self._table)
        self._cr.execute("""
            CREATE view %s as
              %s
              FROM account_move as account_move_line__move_id,account_move_line
                WHERE account_id IN (SELECT id FROM account_account WHERE user_type_id IN (SELECT id from account_account_type WHERE internal_group IN ('expense','income')))  
                    AND ("account_move_line"."move_id"="account_move_line__move_id"."id") 
                    AND (("account_move_line__move_id"."state" = 'posted')  ) 
                %s
        """ % (self._table, self._select(), self._group_by()))

        # for r in self.env.cr.dictfetchall():
        #     pass
