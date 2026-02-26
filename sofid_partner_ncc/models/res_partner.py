from odoo import models, fields

class ResPartner(models.Model):
    _inherit = "res.partner"

    custom_ncc = fields.Char(string=" N°Compte contribualble ")

    def _display_address(self, without_company=False):
        res = super()._display_address(without_company=without_company)

        for partner in self:
            if partner.custom_ncc:
                # On insère street3 après street2
                if partner.street2:
                    res = res.replace(
                        partner.street2,
                        partner.street2 + '\n' + partner.custom_ncc
                    )
                elif partner.street:
                    res = res.replace(
                        partner.street,
                        partner.street + '\n' + partner.custom_ncc
                    )

        return res