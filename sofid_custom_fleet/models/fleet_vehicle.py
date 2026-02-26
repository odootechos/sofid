from odoo import models, fields

class FleetVehicle(models.Model):
    _inherit = 'fleet.vehicle'

    employee_driver_id = fields.Many2one(
        'hr.employee',
        string='Conducteur',
        tracking=True
    )

    employee_future_driver_id = fields.Many2one(
        'hr.employee',
        string='Future Conducteur',
        tracking=True
    )
    fuel_log_count = fields.Integer(
        string='Fuel Logs',
        compute='_compute_fuel_log_count'
    )
    mobility_card = fields.Char(
        related='employee_driver_id.mobility_card',
        string='Carte Carburant',
        store=True,
        readonly=True
    )

    def _compute_fuel_log_count(self):
        for record in self:
            record.fuel_log_count = self.env['sofid.fleet.fuel.log'].search_count([
                ('vehicle_id', '=', record.id)
            ])

    def open_fuel_logs(self):
        self.ensure_one()
        return {
            'type': 'ir.actions.act_window',
            'name': 'Fuel Logs',
            'res_model': 'sofid.fleet.fuel.log',
            'view_mode': 'tree,form',
            'domain': [('vehicle_id', '=', self.id)],
            'context': {
                'default_vehicle_id': self.id,
                'default_mobilite_card': self.mobility_card,
            }
        }