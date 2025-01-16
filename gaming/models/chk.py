from odoo import fields,api,models 
from odoo.exceptions import UserError

class CHK(models.Model):
    _name="check"
    _description="check model"
    
    name=fields.Char(string="name")
    code=fields.Text(string="Code")
    
    @api.depends('code')
    def exe_code(self):
        for record in self:
            try:
                local_var={
                    'self':record,
                    'env':self.env,    
                }
                exec(record.code,{},local_var)
                
                record.write({
                    'name':'Success'
                })
            except Exception as e:
                raise UserError(e)
        return True
    