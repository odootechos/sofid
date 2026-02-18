from odoo import models, fields

class DgiSendConfirmWizard(models.TransientModel):
    _name = 'dgi.send.confirm.wizard'
    _description = "Confirmation d’envoi DGI"

    invoice_id = fields.Many2one('account.move', required=True)

    def action_confirm(self):
        self.ensure_one()
        return self.invoice_id.action_send_to_dgi()