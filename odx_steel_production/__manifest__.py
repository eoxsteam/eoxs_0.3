# -*- coding: utf-8 -*-

{
    'name': 'Steel Production',
    'category': 'Manufacturing',
    'sequence': 13,
    'summary': '',
    'author': 'Odox',
    'website': 'https://www.odoxsofthub.com',
    'version': '13.0.0.0.0',

    # any module necessary for this one to work correctly
    'depends': ['base', 'sale', 'stock', 'mail','account','odx_report_customisation'],

    # always loaded
    'data': [
        'security/ir.model.access.csv',
        'data/sequence.xml',
        'data/mail_template_job_order.xml',
        'security/security.xml',
        'views/steel_production_view.xml',
        'views/job_order.xml',
        'views/back_end.xml',
        # 'views/stock_valuation.xml',
        'reports/barcode_production.xml',
        'reports/barcode_job_order.xml',
        'wizard/cancel_wizard.xml',
        'wizard/jo_cancel_wizard.xml',

    ],
    # only loaded in demonstration mode
    'demo': [
    ],
    'installable': True,
    'auto_install': False,
    'application': False,
}
