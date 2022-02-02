# -*- coding: utf-8 -*-

import logging
_logger = logging.getLogger(__name__)
from odoo import api, fields, models, _


class ResPartner(models.Model):
    _inherit = 'res.partner'

    @api.multi
    def dossier_open(self):
        partner_ids = self.ids
        partner_ids.append(self.env.user.partner_id.id)
        action = self.env.ref('project.open_view_project_all_config').read()[0]
        action['context'] = {
            'default_partner_ids': partner_ids,
        }
        action['domain'] = [('partner_id','in',partner_ids)]
        return action

    dossiers_count = fields.Integer("# Meetings", compute='_compute_dossiers_count')

    @api.multi
    def _compute_dossiers_count(self):
        for partner in self:
            projects = self.env['project.project'].search([('partner_id', '=', partner.id)])
            partner.dossiers_count = len(projects)