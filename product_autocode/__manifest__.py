{
    'name': 'Product Auto Default Code',
    'version': '1.0',
    'author': 'SOFID',
    'depends': ['product'],
    'data': [
        'views/product_template_view.xml',
    ],
    'assets': {
        'web.assets_backend': [
            '/product_autocode/static/src/js/product_code_autofill.js',
        ],
    },
}