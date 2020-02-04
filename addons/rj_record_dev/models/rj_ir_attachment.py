# -*- coding: utf-8 -*-

import logging
_logger = logging.getLogger(__name__)
from odoo import api, fields, models, _


class IrAttachment(models.Model):
    _inherit = 'ir.attachment'

    date_creation = fields.Date('Creation Date',default=fields.Date.context_today)