# -*- coding: utf-8 -*-

from odoo import models, fields, api, _
from odoo.exceptions import AccessError


class ResPartner(models.Model):
    
    _inherit = 'res.partner'
   
    def write(self, vals):
        """
            Allow write access for groups Update Partner information only
        """
        if not self.env.user.has_group("sofid_partner.update_partner_access_res_groups"):
            raise AccessError(_("You don't have access right for update Contact information"))
        return super(ResPartner,self).write(vals)
    
    @api.model
    def create(self, values):
        if 'property_stock_customer' in values and values.get('property_stock_customer') is False:
           customer_location_id = self.env.ref('stock.stock_location_customers')
           values['property_stock_customer'] = customer_location_id.id
        if 'property_stock_supplier' in values and values.get('property_stock_supplier') is False:
           supplier_location_id = self.env.ref('stock.stock_location_suppliers')
           values['property_stock_supplier'] = supplier_location_id.id
        
        return super(ResPartner, self).create(values)