from odoo import models, fields

class ResPartner(models.Model):
    _inherit = 'res.partner'

    warehouse_id = fields.Many2one(
        'stock.warehouse',
        string="Entrepôt préféré",
        help="Entrepôt logistique à utiliser par défaut pour cette adresse de livraison."
    )
