# -*- coding: utf-8 -*-

from odoo import models, fields, api


class AccountTaxe(models.Model):
    _inherit = 'account.tax'
    

    amount_report = fields.Float(required=True, digits=(16, 4), default=0.0, tracking=True)
    
