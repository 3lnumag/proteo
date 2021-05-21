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

    'depends': ['base', 'contacts', 'account', 'l10n_mx_edi', 'lob'],

    'data': [
        'security/groups.xml',
        'security/ir.model.access.csv',
        'views/lob_account_view.xml',
        'views/account_move_view.xml',
        'views/res_partner_view.xml',
        'views/account_journal_view.xml',
        'views/l10n_mx_edi_report_invoice.xml',
        'report/lobextend_reporting_views.xml',
        'wizard/document_wizard.xml',
    ],

    'installable': True,
}
