# -*- coding: utf-8 -*-

{
    'name': 'RJ Records',
    'summary': """Handle RJ expedient records for placing records like file""",
    'description': """
    This module has functionalities inherit from odoo project module with some
    extra functionalities that belongs to the RJ bussiness logic like display of file record.
    """,
    'author': 'aLabs',
    'website': 'https://alabs.org',
    'category': 'Project',
    'license': 'AGPL-3',
    'version': '0.18',
    'installable': True,
    'application': True,

    'depends': [
            'project','base','rj_records','calendar','web_widget_color','web'
    ],

    'data': [
        'security/ir.model.access.csv',
        # 'security/hide_menu_security.xml',
        'views/rj_records.xml',
        'views/clients.xml',
        'views/assets.xml',
        'views/rj_ir_attachment.xml',
        'views/calendar_events.xml',
        'report/project_report.xml',
        'report/account_invoice_report.xml',
        'report/account_income_area_report.xml',

    ],

    'demo': [
    ],
}