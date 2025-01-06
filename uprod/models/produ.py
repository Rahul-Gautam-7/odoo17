from odoo import api,fields,models 

class Prod(models.Model):
    _name="prods"
    _description="product related"
    
    name=fields.Char(string='Name' ,tracking=True)
    ref=fields.Char(string='Product_ID', tracking=True)
    category=fields.Selection([
        ('cons','Consumable'),
        ('stor','Storable'),
        ('combo','Combo'),
        ('serv','Service'),
    ],string='Category', tracking=True)
    price=fields.Integer(string='Price', tracking=True)
    active=fields.Boolean(string='Active', tracking=True)
    