{
    'name':'Game Development',
    'version' : '2.0.3',
    'sequence' : -101,
    'author' : 'Arthur Morgon',
    'summary' : 'THis is game develop',
    'description' : 'Game industry',
    'depends':['mail','product'],
    'data' : [
        'security/ir.model.access.csv',
        'data/seq_view.xml',
        'data/tags_data.xml',
        'data/order_seq.xml',
        'wizard/cancel_view.xml',
        'views/menu.xml','views/game_view.xml','views/gnm_view.xml',
        'views/chk_view.xml',
        'views/res_config_settings_view.xml',
        'views/tags.xml',
    ],
    'installable':True,
    'application' : True
}