{
    'name': 'owl_module',
    'version': '1.0',
    'sequence':-189,
    'description': 'owl module',
    'author': 'Rahul',
    'license': 'LGPL-3',
    'depends': [
      'web','base',  
    ],
    'data': [
        'security/ir.model.access.csv',
        'views/todo_list.xml',
        'views/res_partner.xml',
       
    ],
    'demo': [
        
    ],
    'installable': True,
    'application': True,
    'assets': {
        'web.assets_backend':[
            'owl_module/static/src/components/todo_list/todo_list.js',
            'owl_module/static/src/components/todo_list/todo_list.xml',
            'owl_module/static/src/components/view_inheritance/res_partner_list_view.js',
            'owl_module/static/src/components/view_inheritance/res_partner_list_view.xml',
            'owl_module/static/src/components/view_inheritance/res_partner_kanban_view.js',
            'owl_module/static/src/components/view_inheritance/res_partner_form_view.js',
            'owl_module/static/src/components/view_inheritance/res_partner_form_view.xml',
            'owl_module/static/src/components/view_inheritance/res_partner_kanban_view.xml',
            'owl_module/static/src/components/view_inheritance/res_partner_kanban_view.scss',   
        ]
    }
}