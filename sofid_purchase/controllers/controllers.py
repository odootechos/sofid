# -*- coding: utf-8 -*-
# from odoo import http


# class SofidPurchase(http.Controller):
#     @http.route('/sofid_purchase/sofid_purchase', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/sofid_purchase/sofid_purchase/objects', auth='public')
#     def list(self, **kw):
#         return http.request.render('sofid_purchase.listing', {
#             'root': '/sofid_purchase/sofid_purchase',
#             'objects': http.request.env['sofid_purchase.sofid_purchase'].search([]),
#         })

#     @http.route('/sofid_purchase/sofid_purchase/objects/<model("sofid_purchase.sofid_purchase"):obj>', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('sofid_purchase.object', {
#             'object': obj
#         })
