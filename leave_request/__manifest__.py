{
    'name': 'Leave Request',
    'version': '1.0.12',
    'description': 'This is module for leave request',
    'summary': 'Leave request module',
    'author': 'Rahul',
    'license': 'LGPL-3',
    'sequence':-104,
    'category': '',
    'depends': [
        'hr'
    ],
    'data': [
        'security/security_groups.xml',
        'security/ir.model.access.csv',
        'security/record_rules.xml',
        'views/menu.xml',
        'views/leave_view.xml',
    ],
    'demo': [
        
    ],
    'installable': True,
    'application': True,
    'assets': {
         
    }
}