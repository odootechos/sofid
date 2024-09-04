# -*- coding: utf-8 -*-
{
    'name': "Sofid Account",

    'description': """
        Sofid Account customization addons
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
        'account',
        'base'
    ],

    # always loaded
    'data': [
        # Groups
        'data/groups.xml',
        # Views
        'views/account_journal_dashboard_view.xml',
        # Report
        'report/report_invoice.xml'
    ],
   
}
