# -*- coding: utf-8 -*-
import json
import logging
from email.policy import default

import requests
from odoo import api, fields, models
from odoo.exceptions import UserError
import base64
from odoo.tools import html2plaintext
from odoo.modules.module import get_module_resource


_logger = logging.getLogger(__name__)

class AccountMove(models.Model):
    _inherit = 'account.move'

    # ============================
    # FNE FIELDS
    # ============================
    fne_status = fields.Selection([
        ('draft', 'Brouillon'),
        ('sent', 'Envoyée'),
        ('signed', 'Signée'),
        ('error', 'Erreur'),
    ], default='draft', readonly=True)
    fne_logo = fields.Binary("Logo FNE", compute="_compute_fne_logo")

    fne_reference = fields.Char("Référence FNE", readonly=True)

    fne_token = fields.Char("Token FNE", readonly=True)
    fne_send_date = fields.Datetime("Date d'envoi FNE", readonly=True)
    fne_parent_reference = fields.Char("Référence FNE origine", readonly=True)
    fne_invoiceId = fields.Char("ID FNE", readonly=True)
    fne_refund_reference = fields.Char("Référence FNE Avoir", readonly=True)
    fne_refund_token = fields.Char("Token FNE Avoir", readonly=True)

    fne_payment_method = fields.Selection([
        ('card', 'Carte bancaire'),
        ('check', 'Chèque'),
        ('cash', 'Espèces'),
        ('mobile-money', 'Mobile Money'),
        ('transfer', 'Virement'),
        ('deferred', 'À terme'),
    ], string="Mode de paiement FNE", default='mobile-money')

    fne_template = fields.Selection([
        ('B2B', 'B2B'),
        ('B2C', 'B2C'),
        ('B2F', 'B2F (RNE)'),
    ], string="Type FNE", default='B2C')

    fne_footer = fields.Text("Pied de page", default='SAS au capital de:100 000 000 CFA- Siège:Marcory Zone 4C,RUE Pierre et Marie Curie impasse Elvier 110 - 18 B.P.M. 1534 Abidjan 18 -RCN°CI-ABJ-03-2023-M39360 -Email:contact@sofidci.com www.sofidci.com -C.B:CI00801129012944117236 88')
    fne_global_discount = fields.Float("Remise globale (%)")
    fne_reference_display = fields.Char(
        string="Référence FNE",
        compute='_compute_fne_reference_display',
        store=False
    )
    total_discount = fields.Monetary(
        string='Remise totale',
        compute='_compute_total_discount',
        store=True,
        currency_field='currency_id'
    )
    fne_global_balance = fields.Integer(
        string="Balance FNE",
        help="Balance globale FNE calculée"
    )
    fne_global_balance_display = fields.Char(
        string="Stickers",
        compute="_compute_fne_global_balance_display"
    )


    def _compute_fne_global_balance_display(self):
        for rec in self:
            # Format 1 500 000 FCFA
            rec.fne_global_balance_display = f"{rec.fne_global_balance:,.0f} FCFA"

    def action_show_fne_balance(self):
        return True


    @api.depends('invoice_line_ids.discount_amount')
    def _compute_total_discount(self):
        for inv in self:
            inv.total_discount = sum(inv.invoice_line_ids.mapped('discount_amount'))

    @api.depends('move_type', 'fne_reference', 'fne_refund_reference')
    def _compute_fne_reference_display(self):
        for rec in self:
            if rec.move_type == 'out_refund':
                rec.fne_reference_display = rec.fne_refund_reference
            else:
                rec.fne_reference_display = rec.fne_reference

    # ============================
    # ENDPOINT
    # ============================
    def _get_fne_endpoint(self):
        icp = self.env['ir.config_parameter'].sudo()
        base_url = icp.get_param('sofid_dgi.api_url')
        if not base_url:
            raise UserError("URL API FNE manquante.")
        return f"{base_url}/external/invoices/sign"


    def _compute_fne_logo(self):
        for rec in self:
            if rec.fne_status == "signed":
                # Charger le fichier image depuis le module
                with open(get_module_resource('sofid_dgi', 'static/src/image', 'logofne.png'), 'rb') as f:
                    rec.fne_logo = base64.b64encode(f.read())
            else:
                rec.fne_logo = False

    # ============================
    # GET FNE URL
    # ============================
    def get_fne_url(self):
        """Retourne l'URL de vérification FNE selon le type (facture ou avoir)"""
        self.ensure_one()
        url = self.fne_token if self.move_type == 'out_invoice' else self.fne_refund_token
        if not url:
            raise UserError("Cette facture n’a pas de token FNE. Envoyez-la d'abord à la DGI.")
        return url

    # ============================
    # BUILD ITEMS
    # ============================

    def _build_items(self):
        items = []
        for line in self.invoice_line_ids:
            item = {
                'reference': line.product_id.default_code or '',
                'description': line.name or (line.product_id.name if line.product_id else ''),
                'quantity': abs(float(line.quantity)),
                'amount': float(line.price_unit),
                'discount': float(line.discount or 0),
                'measurementUnit': line.product_uom_id.name or '',
            }
            taxes = []

            for tax in line.tax_ids:
                tax_name = (tax.name or '').upper().strip()

                # Mapping des taxes Odoo vers FNE
                if 'TVA 18% NON FACTURÉE' in tax_name:
                    taxes.append('TVAC')
                elif 'TVA 18.0%' in tax_name:
                    taxes.append('TVA')
                elif 'TVAB' in tax_name:
                    taxes.append('TVAB')
                elif 'TVAD' in tax_name:
                    taxes.append('TVAD')
                elif 'TVAE' in tax_name:
                    taxes.append('TVAE')
                # Sinon, ignorer ou logger l'info
                else:
                    _logger.warning("Taxe non reconnue pour FNE : %s", tax_name)

            item['taxes'] = taxes
            item['customTaxes'] = []
            items.append(item)
        return items
    # ============================
    # BUILD PAYLOAD FACTURE
    # ============================
    def _build_payload(self):
        self.ensure_one()
        clean_narration = "\n" + html2plaintext(self.narration or "").strip()
        clean_ref = self.ref or ""

        commercial_message = " ".join(
            part for part in [clean_ref, clean_narration] if part
        )

        partner = self.partner_id
        company = self.company_id
        template = 'B2B' if partner.is_company else 'B2C'
        if self.fne_template == 'B2F':
            template = 'B2F'

        payload = {
            'invoiceType': 'sale',
            'paymentMethod': self.fne_payment_method,
            'template': template,
            'isRne': template == 'B2F',
            'rne': self.fne_template if template == 'B2F' else '',
            'clientNcc': partner.vat or '',
            'clientCompanyName': partner.name or '',
            'clientPhone': partner.phone or partner.mobile or '',
            'clientEmail': partner.email or '',
            'clientSellerName': self.user_id.name if self.user_id else '',
            'pointOfSale': 'SOFID',
            'establishment': 'SOFID SAS',
            'commercialMessage': commercial_message,
            'footer': self.fne_footer or '',
            'foreignCurrency': self.currency_id.name if self.currency_id != company.currency_id else '',
            'foreignCurrencyRate': 0,
            'items': self._build_items(),
            'customTaxes': [],
            'discount': float(self.fne_global_discount or 0),
        }
        return payload

    # ============================
    # SEND FACTURE
    # ============================
    def action_send_to_dgi(self):
        for inv in self:
            if inv.move_type != 'out_invoice':
                raise UserError("Réservé aux factures client.")
            if inv.state != 'posted':
                raise UserError("La facture doit être comptabilisée avant envoi.")
            if inv.fne_status == 'signed':
                raise UserError("Facture déjà signée.")

            endpoint = inv._get_fne_endpoint()
            api_key = self.env['ir.config_parameter'].sudo().get_param('sofid_dgi.api_key')
            if not api_key:
                raise UserError("Clé API FNE manquante.")

            headers = {
                'Authorization': f'Bearer {api_key}',
                'Content-Type': 'application/json'
            }
            payload = inv._build_payload()
            response = requests.post(endpoint, headers=headers, json=payload, timeout=60)

            if response.status_code not in (200, 201):
                inv.fne_status = 'error'
                raise UserError(f"Erreur FNE : {response.text}")

            data = response.json()
            invoice_data = data.get("invoice", {})

            # -----------------------------
            # 1️⃣ Mise à jour de la facture
            # -----------------------------
            balance_sticker = data.get("balance_sticker")
            try:
                balance_sticker = int(balance_sticker) if balance_sticker else 0
            except:
                balance_sticker = 0

            inv.write({
                'fne_reference': data.get("reference"),
                'fne_token': data.get("token"),
                'fne_global_balance': balance_sticker,
                'fne_status': 'signed',
                'fne_send_date': fields.Datetime.now(),
                'fne_invoiceId': invoice_data.get("id"),
            })

            # ------------------------------------------------
            # 2️⃣ Mise à jour des lignes : récupération itemId
            # ------------------------------------------------
            fne_items = invoice_data.get("items", [])
            if not fne_items:
                raise UserError("La plateforme n’a renvoyé aucun ID de ligne FNE.")

            # Vérification que le nombre de lignes correspond
            if len(inv.invoice_line_ids) != len(fne_items):
                raise UserError("Nombre de lignes FNE différent du nombre de lignes Odoo.")

            # Attribution ligne par ligne
            for line, item in zip(inv.invoice_line_ids, fne_items):
                line.write({
                    'fne_line_id': item.get("id")
                })

    # ============================
    # SEND AVOIR
    # ============================
    def action_send_refund_to_dgi(self):
        self.ensure_one()
        if self.move_type != "out_refund":
            raise UserError("Réservé aux avoirs.")
        if not self.reversed_entry_id:
            raise UserError("Cette facture d'avoir n'est pas liée à une facture d'origine.")

        origin = self.reversed_entry_id
        if not origin.fne_invoiceId:
            raise UserError("ID FNE de la facture d’origine introuvable. La facture doit être envoyée à la FNE.")

        base_url = self.env['ir.config_parameter'].sudo().get_param("sofid_dgi.api_url")
        api_key = self.env['ir.config_parameter'].sudo().get_param("sofid_dgi.api_key")
        headers = {"Authorization": f"Bearer {api_key}", "Content-Type": "application/json"}

        # Construction items
        items = []
        for line in self.invoice_line_ids:
            if not line.fne_line_id:
                raise UserError(f"Ligne '{line.name}' sans ID FNE.")
            items.append({"id": line.fne_line_id, "quantity": abs(line.quantity)})

        payload = {"items": items}

        # Envoi avoir FNE
        refund_url = f"{base_url}/external/invoices/{origin.fne_invoiceId}/refund"
        resp = requests.post(refund_url, headers=headers, json=payload, timeout=60)

        if resp.status_code not in (200, 201):
            self.fne_status = "error"
            raise UserError(f"Erreur FNE : {resp.text}")

        result = resp.json()
        self.write({
            "fne_refund_reference": result.get("reference"),
            "fne_refund_token": result.get("token"),
            "fne_status": "signed",
            "fne_send_date": fields.Datetime.now(),
            "fne_parent_reference": origin.fne_reference,
        })

    # ============================
    # ACTION VIEW FNE
    # ============================
    def action_view_fne_invoice(self):
        self.ensure_one()
        fne_url = self.get_fne_url()
        return {
            'type': 'ir.actions.act_url',
            'name': 'Facture FNE',
            'url': fne_url,
            'target': 'new',
        }
