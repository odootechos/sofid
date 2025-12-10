from odoo import http
from odoo.http import request

class ProductAutoCodeController(http.Controller):

    @http.route('/product_autocode/generate_code', type='json', auth='user')
    def generate_code(self, name):
        code = request.env['product.template'].sudo().generate_default_code(name)
        return {'code': code}