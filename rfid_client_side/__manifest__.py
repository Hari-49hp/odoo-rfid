# -*- coding: utf-8 -*-
{
    'name': "Rfid Client Side",

    'summary': """
        Short (1 phrase/line) summary of the module's purpose, used as
        subtitle on modules listing or apps.openerp.com""",

    'description': """
        Long description of module's purpose
    """,

    'author': "mohamed hamdy",
    'website': "http://projomania.com",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/13.0/odoo/addons/base/data/ir_module_category_data.xml
    # for the full list
    'category': 'Stock',
    'version': '0.1',

    # any module necessary for this one to work correctly
    'depends': ['base','stock','point_of_sale'],

    # always loaded
    'data': [
        'security/ir.model.access.csv',
        'views/rfid.xml',
        'views/rfid_generate_serials.xml',
        'views/templates.xml',
        'views/views.xml',
    ],
    'qweb': ['static/src/xml/list_widget.xml',
             'static/src/xml/buttons.xml',
     ],
    # only loaded in demonstration mode
    'demo': [
        'demo/demo.xml',
    ],
}