from odoo import models, fields, api

class SaleOrder(models.Model):
    _inherit = 'sale.order'

    @api.onchange('partner_id', 'partner_shipping_id')
    def _onchange_partner_set_warehouse(self):
        """Lorsqu'on change le client ou l'adresse de livraison,
        proposer l'entrepôt préféré lié au partenaire ou à son adresse de livraison.
        """
        warehouse = self.partner_shipping_id.warehouse_id or self.partner_id.warehouse_id
        if warehouse:
            self.warehouse_id = warehouse

    @api.onchange('warehouse_id')
    def _onchange_update_partner_shipping(self):
        """Lorsqu'on change manuellement l'entrepôt dans un devis,
        mettre à jour automatiquement l'entrepôt de l'adresse de livraison.
        """
        if self.state in ('draft', 'sent') and self.partner_shipping_id and self.warehouse_id:
            self.partner_shipping_id.warehouse_id = self.warehouse_id