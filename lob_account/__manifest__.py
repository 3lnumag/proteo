# -*- coding: utf-8 -*-
{
    'name': "Extensión de facturación",

    'summary': """LOB y extensión de facturación""",

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
        'report/l10n_mx_edi_report_invoice.xml',
        'report/cfdi.xml',
        'report/payment_reporting_views.xml',
        'wizard/document_wizard.xml',
    ],

    'installable': True,
}
