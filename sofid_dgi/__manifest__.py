{
    "name": "SOFID FNE",
    "version": "1.0",
    "category": "Accounting",
    "author": "SOFID",
    "summary": "Intégration FNE pour les factures client",
    "depends": ["account"],
    "data": [
        "security/ir.model.access.csv",
        "data/ir_config_parameter.xml",
        "views/account_move_view.xml",
        "views/dgi_send_confirm_wizard_views.xml",
        "views/dgi_send_refund_confirm_wizard_views.xml",
        "views/report_invoice_inherit.xml",
    ],
    "assets": {
        'web.assets_backend': [
            'sofid_dgi/static/src/image/logofne.png',
        ],
    },
    "installable": True,
    "application": False,
}
