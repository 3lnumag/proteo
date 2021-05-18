# -*- coding: utf-8 -*-
{
    'name': "Lob extensión de facturación",

    'summary': """Catalogo facturación""",

    'description': """
    """,

    'author': "Wissen",
    'website': "http://www.yourcompany.com",


    'category': 'Uncategorized',
    'version': '14.0.1',

    'depends': ['base', 'contacts', 'account', 'l10n_mx_edi', 'lob', 'base_address_extended'],

    'data': [
        'security/groups.xml',
        'security/ir.model.access.csv',
        'views/lob_account_view.xml',
        'views/account_move_view.xml',
        'views/res_partner_view.xml',
        'views/account_journal_view.xml',
        'views/lob_account_report_invoice.xml',
        'wizard/document_wizard.xml',
    ],

    'installable': True,
}
