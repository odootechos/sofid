# -*- coding: utf-8 -*-
# from odoo import http


# class SofidAccount(http.Controller):
#     @http.route('/sofid_account/sofid_account', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/sofid_account/sofid_account/objects', auth='public')
#     def list(self, **kw):
#         return http.request.render('sofid_account.listing', {
#             'root': '/sofid_account/sofid_account',
#             'objects': http.request.env['sofid_account.sofid_account'].search([]),
#         })

#     @http.route('/sofid_account/sofid_account/objects/<model("sofid_account.sofid_account"):obj>', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('sofid_account.object', {
#             'object': obj
#         })
