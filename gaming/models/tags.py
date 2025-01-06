from odoo import models,api,fields      

class Tags(models.Model):
    _name="tags"
    _description="Tags for use"
    
    
    name=fields.Char(string="Name")
    active=fields.Boolean(string="Active",default=True)
    color=fields.Integer(string="Color")
    color2=fields.Char(string="Color2")
    
    
    _sql_constraints = [
        ('unique_name','unique(name)','Name must be unique')
    ]
        