from odoo import models, fields,api

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

    @api.onchange('employee_driver_id')
    def _onchange_employee_driver_id(self):
        for rec in self:
            if rec.employee_driver_id and rec.employee_driver_id.address_home_id:
                rec.driver_id = rec.employee_driver_id.address_home_id

    @api.model
    def create(self, vals):
        if vals.get('employee_driver_id'):
            employee = self.env['hr.employee'].browse(vals['employee_driver_id'])
            if employee.address_home_id:
                vals['driver_id'] = employee.address_home_id.id
        vehicle = super(FleetVehicle, self).create(vals)
        # Création automatique du log si conducteur défini
        if vehicle.employee_driver_id:
            self.env['fleet.vehicle.assignation.log'].create({
                'vehicle_id': vehicle.id,
                'employee_driver_id': vehicle.employee_driver_id.id,
                'driver_id': vehicle.driver_id.id,
                'date_start': fields.Date.today(),  # date de début de l'assignation
            })
        return vehicle

    def write(self, vals):
        # remplir driver_id avant écriture
        if 'employee_driver_id' in vals and vals['employee_driver_id']:
            employee = self.env['hr.employee'].browse(vals['employee_driver_id'])
            if employee.address_home_id:
                vals['driver_id'] = employee.address_home_id.id

        res = super(FleetVehicle, self).write(vals)

        # créer un log si employee_driver_id changé
        if 'employee_driver_id' in vals:
            for vehicle in self:
                self.env['fleet.vehicle.assignation.log'].create({
                    'vehicle_id': vehicle.id,
                    'employee_driver_id': vehicle.employee_driver_id.id,
                    'driver_id': vehicle.driver_id.id,
                    'date_start': fields.Date.today(),
                })
        return res


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

class FleetVehicleLogServices(models.Model):
    _inherit = 'fleet.vehicle.log.services'

    employee_purchaser_id = fields.Many2one(
        'hr.employee',
        string='Conducteur',
        tracking=True
    )

class FleetVehicleLogContract(models.Model):
    _inherit = 'fleet.vehicle.log.contract'

    employee_purchaser_id = fields.Many2one(
        'hr.employee',
        string='Conducteur',
        tracking=True
    )

class FleetVehicleOdometer(models.Model):
    _inherit = 'fleet.vehicle.odometer'

    employee_driver_id = fields.Many2one(
        'hr.employee',
        string='Conducteur',
        tracking=True
    )

class FleetVehicleAssignationLog(models.Model):
    _inherit = 'fleet.vehicle.assignation.log'

    employee_driver_id = fields.Many2one(
        'hr.employee',
        string='Conducteur',
        tracking=True
    )
    driver_id = fields.Many2one(
        'res.partner',
        string='Conducteur',
        tracking=True,
        required=False,
    )

    @api.model
    def create(self, vals):
        # remplir driver_id à partir de employee_driver_id
        if 'employee_driver_id' in vals and vals['employee_driver_id']:
            employee = self.env['hr.employee'].browse(vals['employee_driver_id'])
            if employee.address_home_id:
                vals['driver_id'] = employee.address_home_id.id
        return super(FleetVehicleAssignationLog, self).create(vals)

    def write(self, vals):
        # idem pour write
        if 'employee_driver_id' in vals and vals['employee_driver_id']:
            employee = self.env['hr.employee'].browse(vals['employee_driver_id'])
            if employee.address_home_id:
                vals['driver_id'] = employee.address_home_id.id
        return super(FleetVehicleAssignationLog, self).write(vals)

