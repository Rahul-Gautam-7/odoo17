from odoo import models,api,fields  

class StudentTag(models.Model):
    _name="student.tag"
    _description="This is the student tag"
    
    
    name=fields.Char(string="Tags")
    active=fields.Boolean(string="Active",default=True)
    color = fields.Integer(string="Colors")
    colors=fields.Char(string="Color")
    sequence=fields.Integer(string="Sequence")
    
    _sql_constraints =[
        ('unique_tag_name','unique (name,active)','Name must be unique'),
        ('check_sequence','check(sequence > 0)','Sequence must be positive')
        
    ]