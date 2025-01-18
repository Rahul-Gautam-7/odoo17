from odoo import api, fields,models 
from odoo.exceptions import UserError 
import logging 


_logger=logging.getLogger(__name__)

class INSI(models.Model):
    _name="in.si"
    _description="check views"
    
    name=fields.Char(string="Names")
    code=fields.Text(string="Code")
    result = fields.Text("Execution Result : ", readonly=True)  
    
    @api.depends('code')
    def action_execute_code(self):
        for record in self:
            try:
                local_vars = {
                    'record':record,
                    'self':record,
                    'env':self.env,  
                }
                exec(record.code, {}, local_vars) 

                result = local_vars.get('result',None)
            
                _logger.info("Execution Result: %s", local_vars)
                record.write({
                    'result': result
                })
            except Exception as e:
                raise UserError(f"Error while executing code: {e}")
        return True
    
    def action_python_code(self):
        for rec in self:
            # vals=self.env['student.library'].search_count(['|',('gender','=','male'),('gender','=','female')])
            # vals=self.env['student.library'].browse(2).get_metadata()
            # vals=self.env['student.library'].browse(2).fields_get(['name','gender'])
            # vals=self.env['student.library'].with_context(active_test=False).search_count([])
            vals=self.env['student.library'].search_count([])
            _logger.info(vals)
    