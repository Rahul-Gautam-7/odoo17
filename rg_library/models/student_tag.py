from odoo import models,api,fields,_  

class StudentTag(models.Model):
    _name="student.tag"
    _description="This is the student tag"
    
    
    name=fields.Char(string="Tags")
    active=fields.Boolean(string="Active",default=True)
    color = fields.Integer(string="Colors")
    colors=fields.Char(string="Color")
    sequence=fields.Integer(string="Sequence")
    
    @api.returns('self', lambda value: value.id)
    def copy(self, default=None):
        if default is None:
            default = {}
        if not default.get('name'):
            default['name'] = _("%s (copy)", self.name)
        
        return super(StudentTag,self).copy(default)
        

            
    
    _sql_constraints =[
        ('unique_tag_name','unique (name,active)','Name must be unique'),
        ('check_sequence','check(sequence > 0)','Sequence must be positive')   
    ]
    
    