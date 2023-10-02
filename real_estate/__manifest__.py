# -*- coding: utf-8 -*-
{
    'name': "Real Estate",
    
    'summary': """
        Real Estate Managmment System""",
    
    'category': 'Real Estate Brokerage',
    
    'depends': ['base'],
    
    'data': [
        'views/estate_property_view.xml',
        'views/estate_property_type_view.xml',
        'views/estate_property_tags_view.xml',
        'views/estate_property_offer_view.xml',
        'views/estate_menus.xml',
        #'views/res_users_views.xml',
        'security/security.xml',
        'security/ir.model.access.csv',
        'data/estate.property.type.csv',
        'report/estate_offers_report.xml',
    ],
    
    'demo': [
        'demo/demo.xml',
    ],
    
    'application':['True'],
}
