# -*- coding: utf-8 -*-

import logging
_logger = logging.getLogger(__name__)
from odoo import api, fields, models, tools,_
from odoo.exceptions import UserError,ValidationError


class ProjectProject(models.Model):
    _inherit = 'project.project'

    file_attachment = fields.Many2many('ir.attachment',compute="compute_get_attached_file",string="File(s)")
    other_payer = fields.Many2one('res.partner', string="Other Payer")
    physical_box = fields.Integer("Physical Box",help="Enter 4 digits")

    @api.constrains('physical_box')
    def _constaint_physical_box(self):
        if len(str(self.physical_box)) != 4:
            raise ValidationError(_('Physical Box must contain 4 digits numeric'))

    def compute_get_attached_file(self):
        file_list = []
        for s in self:
            file_id = self.env['ir.attachment'].search([('res_id','=',s.id)])
            # file_list.append(file_id.ids)
            s.file_attachment=file_id.ids
            print(file_list)

    @api.model
    def create(self, vals):
        sequence = self.env.ref('rj_record_dev.ir_sequence_project_number')
        apha = str(sequence.next_by_id())
        vals['name'] = apha+' - '+ vals['name']
        vals['code'] = apha
        result = super(ProjectProject, self).create(vals)
        return result


class ReportProjectTaskUser(models.Model):
    _inherit = "report.project.task.user"

    project_task = fields.Many2one('project.task',string="Task")
    planned_hours = fields.Char('Planned Hours', readonly=True)
    # complexity = fields.Float('Complexity', readonly=True)

    def _select(self):
        return super(ReportProjectTaskUser, self)._select() + """,t.planned_hours"""
        

    def _group_by(self):
        group_by_str = """
                    GROUP BY
                        t.id,
                        
                       
                        date_end,
                        date_deadline,
                        date_last_stage_update,
                        t.user_id,
                        t.project_id,
                        t.priority,
                        t.planned_hours,
                       
                        t.company_id,
                        t.partner_id,
                        stage_id,
                        planned_hours
                """
        return group_by_str

    @api.model_cr
    def init(self):
        tools.drop_view_if_exists(self._cr, self._table)
        self.env.cr.execute("""
            CREATE view %s as
                      %s
                      FROM project_task t JOIN project_project p ON t.project_id = p.id
                        WHERE t.active = 'true' AND state='open'
                        %s
                """ % (self._table, self._select(), self._group_by()))
