# -*- coding: utf-8 -*-
{
    'name': "Sofid Sale",

    'description': """
        Sofid Sale customization addons
    """,

    'author': "Arkeup",
    'website': "https://arkeup.com",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/15.0/odoo/addons/base/data/ir_module_category_data.xml
    # for the full list
    'category': 'Uncategorized',
    'version': '15.0.0.1',

    # any module necessary for this one to work correctly
    'depends': [
        'base',
        'sale'
    ],

    # always loaded
    'data': [
        # report
        'report/sale_report_templates.xml'
    ]
}
