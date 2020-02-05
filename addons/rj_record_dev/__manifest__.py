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
    'version': '0.2',
    'installable': True,
    'application': True,

    'depends': [
            'project','base','rj_records'
    ],

    'data': [
        'views/rj_records.xml',
        'views/clients.xml',
        'views/rj_ir_attachment.xml',
    ],

    'demo': [
    ],
}