from odoo import models, fields, api


class FleetFuelLog(models.Model):
    _name = 'sofid.fleet.fuel.log'
    _description = 'Fleet Fuel Log'
    _order = 'date desc'

    vehicle_id = fields.Many2one(
        'fleet.vehicle',
        string='Vehicle',
        required=True,
        ondelete='cascade'
    )

    mobility_card = fields.Char(
        related="vehicle_id.mobility_card",
        string='Carte Carburant',
        store = True,
        readonly = True
    )

    supplier_id = fields.Many2one(
        'res.partner',
        string='Fournisseur'
    )

    liters = fields.Float(
        string='Liters',
        required=True
    )

    fuel_type = fields.Selection(
        related='vehicle_id.fuel_type',
        string='Fuel Type',
        store=True
    )

    date = fields.Date(
        string='Date',
        default=fields.Date.today,
        required=True
    )

    @api.onchange('vehicle_id')
    def _onchange_vehicle(self):
        if self.vehicle_id:
            self.mobility_card = self.vehicle_id.mobility_card
