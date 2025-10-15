{
    'name': 'Custom Proforma Sale Order Report',
    'version': '16.0.1.0.0',
    'category': 'Sales',
    'summary': 'Customisation du rapport proforma (cachet).',
    'description': """
        Ce module permet d'ajouter :
        - Le cachet de l'entreprise en bas du PDF proforma
    """,
    'author': 'SOFID',
    'depends': ['sale'],
    'data': [
        'views/report_saleorder.xml',
    ],
    'assets': {
        'web.report_assets_common': [
            'sale_order_proforma_custom/static/img/signature.jpg',
        ],
    },
    'installable': True,
    'application': False,
    'license': 'LGPL-3',
}
