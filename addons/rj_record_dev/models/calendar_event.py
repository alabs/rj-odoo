# -*- coding: utf-8 -*-

from odoo import api, fields, models

class CalendarEventProject(models.Model):
    _inherit = 'project.task'

    calendar_id = fields.Many2one('calendar.event',string="Meetings")
    calen_tag = fields.Char("Calendar Tag",related="tag_ids.name")
    color = fields.Char("Mark Color")

    @api.onchange('calendar_id')
    def onchange_calendar(self):
        self.name = self.calendar_id.name
        self.calen_tag = self.calendar_id.categ_ids.name


class CalendarEvents(models.Model):
    _inherit = 'calendar.event'

    @api.model
    def create(self, vals):
        res = super(CalendarEvents, self).create(vals)
        project =  self.env['project.task'].create({'name':vals.get('name'),
                                                    'calendar_id':res.id,
                                                    'date_deadline':vals.get('stop')
                                                    })
        print(project)
        return res