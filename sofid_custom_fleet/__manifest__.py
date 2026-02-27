{
    'name': 'SOFID Custom Fleet',
    'version': '1.0',
    'summary': 'Custom Fleet Enhancements for SOFID',
    'author': 'SOFID',
    'category': 'Fleet',
    'depends': [
        'fleet',
        'hr',
    ],
    'data': [
        'security/ir.model.access.csv',
        'views/fleet_vehicle_views.xml',
        'views/fleet_employee_inherit.xml',
        'views/fleet_vehicle_model_views.xml',
        'views/fleet_fuel_log_views.xml'
    ],
    'installable': True,
    'application': False,
}
