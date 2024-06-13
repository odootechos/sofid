# -*- coding: utf-8 -*-

from odoo import models, fields, api
from num2words import num2words


class SaleOrder(models.Model):
    _inherit = 'sale.order'
   
    def convert_price_to_word(self, price):
        """
            Convert price to word
            return: string
        """
        return num2words(price, lang='fr')
