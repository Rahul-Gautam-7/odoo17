{
    'name': 'owl_module',
    'version': '1.0',
    'sequence':-189,
    'description': 'owl module',
    'author': 'Rahul',
    'license': 'LGPL-3',
    'depends': [
      'web'  
    ],
    'data': [
        'security/ir.model.access.csv',
        'views/todo_list.xml',
       
    ],
    'demo': [
        
    ],
    'installable': True,
    'application': True,
    'assets': {
        'web.assets_backend':[
            'owl_module/static/src/components/todo_list/todo_list.js',
            'owl_module/static/src/components/todo_list/todo_list.xml',
           
        ]
    }
}