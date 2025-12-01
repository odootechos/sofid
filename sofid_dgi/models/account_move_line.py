from odoo import models, fields,api

class AccountMoveLine(models.Model):
    _inherit = "account.move.line"

    fne_line_id  = fields.Char("ID FNE Article")

    discount_amount = fields.Monetary(
        string='Prix remisé',
        compute='_compute_discount_amount',
        store=True,
        currency_field='currency_id'
    )

    @api.depends('quantity', 'price_unit', 'discount', 'currency_id')
    def _compute_discount_amount(self):
        for line in self:
            line.discount_amount = (line.quantity or 0.0) * (line.price_unit or 0.0) * ((line.discount or 0.0) / 100.0)
