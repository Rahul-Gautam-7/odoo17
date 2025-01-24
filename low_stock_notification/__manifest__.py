{
    'name': 'Low Stock Notification',
    'version': '1.0',
    'description': 'module for low stock ',
    'summary': 'low stock notify',
    'author': 'Rahul',
    'license': 'LGPL-3',
    'depends': [
        'product','base'
    ],
    'data': [
        'security/ir.model.access.csv',
        'views/menu.xml',
        'views/low_view.xml',
        'views/res_config_setting.xml',
        'views/cron.xml',
        
    ],
    'demo': [
        
    ],
    'installable': True,
    'application': True,
    
}