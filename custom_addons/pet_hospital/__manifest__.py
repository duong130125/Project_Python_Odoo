# -*- coding: utf-8 -*-
{
    'name': "pet_hospital",
    'summary': "Short (1 phrase/line) summary of the module's purpose",
    'description': """
Long description of module's purpose
    """,
    'author': "Dương",
    'website': "https://www.yourcompany.com",
    'category': 'Uncategorized',
    'version': '0.2',
    'depends': ['base', 'product', 'mail'],
    'data': [
        'security/pet_security.xml',
        'security/ir.model.access.csv',
        'data/ir_sequence_data.xml',
        'views/pet_views.xml',
        'views/pet_booking_views.xml',
        'views/pet_appointment_views.xml',
        'views/res_partner_views.xml',
        'views/product_views.xml',
        'data/demo_data.xml',
        'views/menus.xml',
    ],
    'demo': [
        'demo/demo.xml',
    ],
}

