# -*- coding: utf-8 -*-
{
    'name': "Import Lot Serial Numbers",

    'summary': """
        Helps to import lot and serial numbers """,

    'description': """
        helps to manage traceability of the product
    """,

    'author': "Minions 6",

    'version': '15.0.1.0',
    'depends': ['base', 'stock'],

    'data': [
        'security/ir.model.access.csv',
        'views/stock_production_lot_inherit_views.xml',
    ],
}
