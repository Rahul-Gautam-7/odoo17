from odoo import models,api,fields , _ 

class Tags(models.Model):
    _name="tags"
    _description="Tags for use"
    
    
    name=fields.Char(string="Name")
    active=fields.Boolean(string="Active",default=True)
    color=fields.Integer(string="Color")
    color2=fields.Char(string="Color2")
    
    @api.returns('self',lambda value:value.id)
    def copy(self,default=None):
        if default is None:
            default={}
        if not default.get('name'):
            default['name'] = _("%s (copy)",self.name)
        return super(Tags,self).copy(default)
    
    
    _sql_constraints = [
        ('unique_name','unique(name)','Name must be unique')
    ]
        