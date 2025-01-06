{
    'name' : 'transport mod',
    'version' : '1.0.2',
    'author' : 'Rahul Gautam',
    'sequence' : -101,
    'depends':['mail'],
    'data' : [
            'security/ir.model.access.csv',
            'views/menu.xml',
            'views/transport.xml',
            'views/test.xml'
        ],
    'summary' : " It is transport module ",
    'description' : " Transportation module ",
    'installable' : True,
    'application' : True 
}