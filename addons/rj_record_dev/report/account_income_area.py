# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import fields, models, tools


class ReportAccountReport(models.Model):
    _name = "report.account.income.area"
    _description = "Account Income Area"
    _order = 'name desc'
    _auto = False

    name = fields.Char(string='Project Title', readonly=True)
    nbr = fields.Integer('# of Tasks', readonly=True)
    income = fields.Float('Income', readonly=True)
    income_percentage = fields.Float('Income %', readonly=True)
    average = fields.Float('Average',group_operator = 'avg', readonly=True)
    area = fields.Many2one('rj_records.area',string="Area")
    date_time = fields.Datetime('Intervals')
    company_id = fields.Many2one('res.company', string='Company', required=True,
                                 default=lambda self: self.env.user.company_id)
    lawyer_id = fields.Many2one('res.users',string="Lawyer",group_operator = 'lawyer_id',store=True)



    # def _select(self):
    #     select_str = """
    #          SELECT
    #                 (select 1 ) AS nbr ,
    #                 p.user_id as lawyer_id,
    #                 p.area_id as area,
    #                 aml.id as id,
    #                 aml.account_id as account_id,
    #                 aml.create_date as date_time,
    #                 COALESCE(SUM(debit),0) - COALESCE(SUM(credit), 0) as balance,
    #                 COALESCE(SUM(debit), 0) as debit,
    #                 COALESCE(SUM(credit), 0) as income,
    #                 AVG(credit) as average,
    #                 (SUM(credit) * 100)::numeric /(SELECT SUM(aml.credit) FROM account_move_line as aml,account_move as account_move_line__move_id,project_project as p, account_invoice as ai WHERE aml.account_id IN (SELECT id FROM account_account WHERE user_type_id IN (SELECT id from account_account_type WHERE internal_group IN ('expense','income'))) AND ("aml"."move_id"="account_move_line__move_id"."id") AND (("account_move_line__move_id"."state" = 'posted')  )
    #                     AND (("aml"."invoice_id" = "ai"."id")  )
    #                     AND (("ai"."project_id" = "p"."id")  )  ) AS income_percentage
    #     """
    #     return select_str

    def _select(self):
        select_str = """
             SELECT
                    (select 1 ) AS nbr ,
                    ai.user_id as lawyer_id,
                    p.area_id as area, 
                    ai.id as id,
                    ai.date_invoice as date_time,
                    SUM(ai.amount_total) as income,
                    AVG(ai.amount_total) as average,
                    (SUM(ai.amount_total) * 100)::numeric /(SELECT SUM(amount_total)
 FROM account_invoice 
 WHERE state='paid' AND type='out_invoice' ) AS income_percentage
        """
        return select_str

    def _group_by(self):
        group_by_str = """
                GROUP BY p.area_id,ai.user_id,ai.id,ai.date_invoice
                  

        """
        return group_by_str

    # def init(self):
    #     tools.drop_view_if_exists(self._cr, self._table)
    #     self._cr.execute("""
    #         CREATE view %s as
    #           %s
    #           FROM account_move as account_move_line__move_id,account_move_line as aml,project_project as p, account_invoice as ai
    #             WHERE aml.account_id IN (SELECT id FROM account_account WHERE user_type_id IN (SELECT id from account_account_type WHERE internal_group IN ('expense','income')))
    #             AND ("aml"."move_id"="account_move_line__move_id"."id")
    #             AND (("account_move_line__move_id"."state" = 'posted')  )
    #             AND (("aml"."invoice_id" = "ai"."id")  )
    #             AND (("ai"."project_id" = "p"."id")  )
    #             %s
    #     """ % (self._table, self._select(), self._group_by()))

    def init(self):
        tools.drop_view_if_exists(self._cr, self._table)
        self._cr.execute("""
            CREATE view %s as
              %s
              From account_invoice as ai, project_project as p where ai.state = 'paid' AND ai.type='out_invoice'  AND ai.project_id = p.id
               %s
        """ % (self._table, self._select(), self._group_by()))
