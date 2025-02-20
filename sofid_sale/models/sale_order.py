# -*- coding: utf-8 -*-

from odoo import models, fields, api, _
from odoo.exceptions import ValidationError

class SaleOrder(models.Model):
    _inherit = 'sale.order'
    
    purchase_order_ids = fields.Many2many('purchase.order')
   
# class SaleOrderLine(models.Model):
#     _inherit = 'sale.order.line'

#     @api.constrains('product_uom_qty')
#     def _check_product_uom_qty(self):
#         for record in self:
#             import pudb;pudb.set_trace()
#             if not isinstance(record.product_uom_qty, int) or record.product_uom_qty != int(record.product_uom_qty):
#                 raise ValidationError(_("Please re-enter the quantity: this field must be an integer."))