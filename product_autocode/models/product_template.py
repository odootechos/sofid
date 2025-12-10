from odoo import models, fields, api

class ProductTemplate(models.Model):
    _inherit = "product.template"

    @api.model
    def _get_next_code(self, name):
        """Génère un code basé sur le nom et l'ID suivant."""
        prefix = (name or '').strip().upper()[:3] or "XXX"
        last_product = self.search([], order='id desc', limit=1)
        next_id = (last_product.id or 0) + 1
        return f"{prefix}{next_id}"

    @api.onchange('name')
    def _onchange_name_generate_code(self):
        """Remplit automatiquement le default_code à la saisie."""
        for record in self:
            if record.name and not record.default_code:
                record.default_code = self._get_next_code(record.name)

    @api.model
    def create(self, vals):
        """Assure que le code reste enregistré même après sauvegarde."""
        if not vals.get('default_code') and vals.get('name'):
            vals['default_code'] = self._get_next_code(vals['name'])
        return super().create(vals)