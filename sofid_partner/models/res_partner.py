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