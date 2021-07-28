# -*- coding: utf-8 -*-
{
    'name': "pmt",

    'summary': """
        Short (1 phrase/line) summary of the module's purpose, used as
        subtitle on modules listing or apps.openerp.com""",

    'description': """
        Long description of module's purpose
    """,

    'author': "My Company",
    'website': "http://www.yourcompany.com",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/12.0/odoo/addons/base/data/ir_module_category_data.xml
    # for the full list
    'category': 'Uncategorized',
    'version': '0.1',

    # any module necessary for this one to work correctly
    'depends': ['base', 'mail'],

    # always loaded
    'data': [
        'security/security.xml',
        'security/ir.model.access.csv',
        'views/views.xml',
        'views/perspective_views.xml',
        'views/corevalues_views.xml',
        'views/survey_views.xml',
        'views/orgbranch_views.xml',
        'views/corerating_views.xml',
        'views/valuerating_views.xml',
        'wizard/complete_profile_views.xml',
        'views/resusers_views.xml',
        'views/templates.xml',
        'report/appraisal_report.xml',
        'report/appraisal_report_template.xml',
        'data/report_paper_format.xml',
    ],
    # only loaded in demonstration mode
    'demo': [
        'demo/demo.xml',
    ],
}