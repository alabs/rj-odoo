# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import fields, models, tools


class ReportProjectStageUser(models.Model):
    _name = "report.project.task.stage"
    _description = "Project Stage"
    _order = 'name desc'
    _auto = False

    name = fields.Char(string='Project Title', readonly=True)
    nbr = fields.Integer('# of Tasks', readonly=True)
    user_id = fields.Many2one('res.users', string='Assigned To', readonly=True)
    managers_ids = fields.Many2many('res.users', string='Assigned To', readonly=True)
    complexity = fields.Float('Complexity', readonly=True)

    state = fields.Selection([
            ('open', 'Abierto'),
            ('closed', 'Cerrado'),
            ('sleep', 'Dormido')
        ], string='Kanban State', readonly=True)

    def _select(self):
        select_str = """
             SELECT
                    (select 1 ) AS nbr,t.name ,CAST(coalesce(t.complexity, '0') AS float) as complexity,
                    t.id as id ,p.project_id as project_id,
                    p.user_id as user_id,t.state as state

        """
        return select_str

    def _group_by(self):
        group_by_str = """
                GROUP BY
                    t.id,p.project_id,p.user_id,t.state,t.complexity,t.name
                    
        """
        return group_by_str

    def init(self):
        tools.drop_view_if_exists(self._cr, self._table)
        self._cr.execute("""
            CREATE view %s as
              %s
              FROM expedient_managers_users_rel p JOIN project_project as t ON p.project_id = t.id
              WHERE t.state = 'open'
                %s
        """ % (self._table, self._select(), self._group_by()))
