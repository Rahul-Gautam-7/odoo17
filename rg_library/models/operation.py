from odoo import api,fields,models 

class Operation(models.Model):
    _name="lib.operation"
    _description="Library operation"
    _log_access=False 
    _rec_name="operation_name"
    
    operation_name=fields.Char(string="Operation")
    lib_id=fields.Many2one('res.users',string="Librarian")
    
    
    @api.model
    def name_create(self,name):
        return self.create({'operation_name':name}).name_get()[0]
    
