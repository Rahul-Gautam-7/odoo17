from odoo import fields,api,models 

class CHK(models.Model):
    _name="check"
    _description="check model"
    
    name=fields.Char(string="name")
    