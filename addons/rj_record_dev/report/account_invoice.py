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
    income = fields.Float('Income', readonly=True)
    expense = fields.Float('Expense', readonly=True)
    date_time = fields.Datetime('Intervals')
    company_id = fields.Many2one('res.company', string='Company', required=True,
                                 default=lambda self: self.env.user.company_id)

    def _select(self):
        select_str = """
             SELECT
                    (select 1 ) AS nbr ,account_move_line.id as id,account_id as account_id,account_move_line.create_date as date_time, 
                    COALESCE(SUM(debit),0) - COALESCE(SUM(credit), 0) as balance, 
                    COALESCE(SUM(debit), 0) as expense, COALESCE(SUM(credit), 0) as income 

        """
        return select_str

    def _group_by(self):
        group_by_str = """
                GROUP BY
                    account_id,
                    account_move_line.id,
                    date_time

        """
        return group_by_str

    def init(self):
        tools.drop_view_if_exists(self._cr, self._table)
        self._cr.execute("""
            CREATE view %s as
              %s
              FROM account_move as account_move_line__move_id,account_move_line
              WHERE account_id IN (SELECT id FROM account_account WHERE user_type_id IN (SELECT id from account_account_type WHERE internal_group IN ('income','expense')))  
               AND ("account_move_line"."move_id"="account_move_line__move_id"."id") 
	            AND (("account_move_line__move_id"."state" = 'posted')  ) 
                %s
        """ % (self._table, self._select(), self._group_by()))
