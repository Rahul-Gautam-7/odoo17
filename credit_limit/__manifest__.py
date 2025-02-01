{
    'name': 'Credit Limit',
    'version': '1.0',
    'description': 'Hold the credit limit',
    'summary': 'Hold the credit limit',
    'author': 'rahul gautam',
    'license': 'LGPL-3',
    'depends': [
        'base','sale','report_xlsx',
    ],
    'data': [
        'security/ir.model.access.csv',
        'views/credit_view.xml',
        'views/popup_view.xml',
        'views/hold_view.xml',
        'data/cust_repor_aciton.xml'
    
    ],
    'demo': [
        
    ],
    'installable': True,
    'application': True,
    'assets': {
        
    }
}