# -*- coding: utf-8 -*-
{
    'name': "sofid_stock",

    'description': """
        Manage SOFID stock
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
        'stock'
    ],

    # always loaded
    'data': [
        # Security
        'security/res_groups.xml',
        # Views
        'views/stock_picking_views.xml',
        'views/stock_quant_views.xml'
    ],
    # only loaded in demonstration mode
    'demo': [
        'demo/demo.xml',
    ],
}
