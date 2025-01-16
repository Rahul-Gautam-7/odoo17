from odoo import api,fields,models 

class Operation(models.Model):
    _name="lib.operation"
    _description="Library operation"
    _log_access=False 
    _rec_name="operation_name"
    _order='sequence,id'
    
    operation_name=fields.Char(string="Operation")
    lib_id=fields.Many2one('res.users',string="Librarian")
    record_reference=fields.Reference(selection=[('student.library','student'),('enroll.stud','Enrollment')],string="Record")
    
    sequence=fields.Integer(string="Sequence",default=1)

    
    
    
    @api.model
    def name_create(self,name):
        return self.create({'operation_name':name}).name_get()[0]
    
