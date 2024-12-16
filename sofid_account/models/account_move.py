# -*- coding: utf-8 -*-

from odoo import models, fields, api
from odoo.tools.misc import formatLang


class AccountMove(models.Model):
    _inherit = 'account.move'
    
    def get_tax_no_invoiced(self, invoice_line_ids):
        # for line in invoice_line_ids:
        tax_ids = invoice_line_ids.tax_ids
        tax_not_invoiced_json = []
        for tax in tax_ids:
            if tax.amount_type != 'group':
                amount_total_list = [
                    tax.amount_report if tax.amount_type == 'fixed' else line.quantity*line.price_unit*tax.amount_report/100
                    for line in invoice_line_ids
                ]
                tax_not_invoiced_json.append({
                    'tax': tax.name,
                    'tax_amount': formatLang(self.env, sum(amount_total_list), currency_obj=self.currency_id)
                })
        return tax_not_invoiced_json
    
