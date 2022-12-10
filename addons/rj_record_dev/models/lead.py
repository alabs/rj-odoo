# -*- coding: utf-8 -*-

import logging
_logger = logging.getLogger(__name__)
from odoo import api, fields, models, _


class Lead(models.Model):
    _inherit = 'crm.lead'

    area_color = fields.Char("Area Color")

    @api.onchange('area_id')
    def area_colors(self):
        for rec in self:
            if rec.area_id.color:
                # rec.color = int(rec.area_id.color)
                # rec.color = 1
                self.write({'color':rec.area_id.color})
                rec.area_color = rec.area_id.color
                print('cc',rec.color)
                print('ac',rec.area_color)

    @api.multi
    def write(self, vals):
        if self.area_id.color:
            vals['color'] = self.env['rj_records.area'].search([('id','=',vals.get('area_id'))]).color
        return super(Lead, self.sudo()).write(vals)


