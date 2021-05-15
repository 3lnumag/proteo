# -*- coding: utf-8 -*-
{
    'name': "Extensión LOB",

    'summary': """Extensión de Líneas de negocio""",

    'description': """
        Módulo que extiende las funcionalidades del modulo lob
    """,

    'author': "Wissen",
    'website': "http://www.yourcompany.com",


    'category': 'Uncategorized',
    'version': '14.0.1',

    'depends': ['sale_management', 'purchase', 'product', 'lob', 'contacts', 'sale_stock', 'mrp', 'lob_account'],

    'data': [
        'security/groups.xml',
        'security/ir.model.access.csv',
        'views/sale_order_view.xml',
        'views/purchase_order_view.xml',
        'views/product_template_view.xml',
        'views/res_partner_view.xml',
        'views/mrp_production_view.xml',
        'report/lobextend_reporting_views.xml',
        'data/lob_extend_data.xml',
    ],
    'installable': True,
}
