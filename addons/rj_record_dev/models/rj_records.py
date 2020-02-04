# -*- coding: utf-8 -*-

import logging
_logger = logging.getLogger(__name__)
from odoo import api, fields, models, _


class ProjectProject(models.Model):
    _inherit = 'project.project'

    file_attachment = fields.Many2many('ir.attachment',compute="compute_get_attached_file",string="File(s)")
    other_payer = fields.Many2one('res.partner', string="Other Payer")

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
        vals['name'] = str(sequence.next_by_id())+' - '+ vals['name']
        result = super(ProjectProject, self).create(vals)
        return result