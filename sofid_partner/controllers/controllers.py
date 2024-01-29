# -*- coding: utf-8 -*-
# from odoo import http


# class SofidPartner(http.Controller):
#     @http.route('/sofid_partner/sofid_partner', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/sofid_partner/sofid_partner/objects', auth='public')
#     def list(self, **kw):
#         return http.request.render('sofid_partner.listing', {
#             'root': '/sofid_partner/sofid_partner',
#             'objects': http.request.env['sofid_partner.sofid_partner'].search([]),
#         })

#     @http.route('/sofid_partner/sofid_partner/objects/<model("sofid_partner.sofid_partner"):obj>', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('sofid_partner.object', {
#             'object': obj
#         })
