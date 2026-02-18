from odoo import models, fields

class DGISendRefundConfirmWizard(models.TransientModel):
    _name = "dgi.send.refund.confirm.wizard"
    _description = "Confirmation d’envoi d’avoir à la DGI"

    invoice_id = fields.Many2one('account.move', string="Avoir", required=True)

    def action_confirm_refund(self):
        self.ensure_one()
        if not self.invoice_id:
            return
        # Appelle la méthode d'envoi spécifique aux avoirs
        self.invoice_id.action_send_refund_to_dgi()
        return {"type": "ir.actions.act_window_close"}