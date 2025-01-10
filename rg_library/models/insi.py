from odoo import api, fields,models 

class INSI(models.Model):
    _name="in.si"
    _description="check views"
    
    name=fields.Char(string="Names")
    code=fields.Text(string="Code")
    