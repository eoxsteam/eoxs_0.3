# -*- coding: utf-8 -*-
{
    'name': "Odx Steel Customisation",

    'summary': """
        Short (1 phrase/line) summary of the module's purpose, used as
        subtitle on modules listing or apps.openerp.com""",

    'description': """
        Long description of module's purpose
    """,

    'author': "Odox",
    'website': "https://www.odoxsofthub.com",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/13.0/odoo/addons/base/data/ir_module_category_data.xml
    # for the full list
    'category': 'Uncategorized',
    'version': '0.1',

    # any module necessary for this one to work correctly
    'depends': ['base','sale_management','purchase','stock','sale_order_lot_selection','stock_restrict_lot'],

    # always loaded
    'data': [
        'security/ir.model.access.csv',
        'data/sequence.xml',
        'views/product.xml',
        'views/purchase_view.xml',
        'views/stock_move_line.xml',
        'views/partner_view.xml',
        'views/stock_lot_view.xml',
        'views/sale_view.xml',
        'views/stock_picking_view.xml',
        'views/account_move.xml',
        'wizard/purchase_line_wizard.xml',
    ],
}
