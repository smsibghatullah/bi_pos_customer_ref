# -*- coding: utf-8 -*-
{
    'name': "bi_pos_customer_ref",

    'summary': """
        Short (1 phrase/line) summary of the module's purpose, used as
        subtitle on modules listing or apps.openerp.com""",

    'description': """
        Long description of module's purpose
    """,

    'author': "My Company",
    'website': "https://www.yourcompany.com",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/16.0/odoo/addons/base/data/ir_module_category_data.xml
    # for the full list
    'category': 'Uncategorized',
    'version': '0.1',

    # any module necessary for this one to work correctly
    'depends': ['base','point_of_sale','web','account','l10n_sa','sale','sale_management','sales_team'],

    # always loaded
    'data': [
        'demo/demo.xml',
        'views/templates.xml',
        'views/views.xml',
    ],
'assets': {
        'point_of_sale.assets': [
            'bi_pos_customer_ref/static/src/js/CustomerReferenceField.js',
            'bi_pos_customer_ref/static/src/xml/pos.xml',
        ],
    },
    # only loaded in demonstration mode
    'demo': [
        'demo/demo.xml',
    ],
}
