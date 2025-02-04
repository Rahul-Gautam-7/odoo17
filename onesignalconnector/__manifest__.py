{
    'name': 'One Signal Connector',
    'version': '1.0',
    'description': 'It connects onesignal with odoo',
    'summary': ' onesignal x odoo',
    'sequence':-111,
    'author': 'Rahul Gautam',
    'license': 'LGPL-3',
    'depends': [
        'base'
    ],
    'data': [
        'security/ir.model.access.csv',
        'views/menu.xml',
        'views/signal_view.xml',
        'views/cron.xml',
        'views/users.xml',
    ],
    'demo': [
        
    ],
    'installable': True,
    'application': True,
    'assets': {
        
    }
}