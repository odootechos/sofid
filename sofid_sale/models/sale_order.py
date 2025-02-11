# -*- coding: utf-8 -*-

from odoo import models, fields, api


class SaleOrder(models.Model):
    _inherit = 'sale.order'
    
    purchase_order_ids = fields.Many2many('purchase.order')
   
