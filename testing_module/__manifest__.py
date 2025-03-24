{
    'name': 'Testing Module',
    'version': '1.0',
    'description': 'Testing module',
    'author': 'Rahul Gautam',
    'sequence':-144,
    'license': 'LGPL-3',
    'depends': [
        'base','website'
    ],
    'data': [
        'security/ir.model.access.csv',
        'views/views.xml',
        'views/templates.xml',
    ],
    'installable': True,
    'application': True,

}