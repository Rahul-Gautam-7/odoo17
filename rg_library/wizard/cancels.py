from odoo import models,api,fields 
import logging 
from datetime import date
from odoo.exceptions import ValidationError
from dateutil import relativedelta

_logger=logging.getLogger(__name__)

class CancelsIssue(models.TransientModel):
    _name="cancel.issue"
    _description="cancel the issued book"
    
    enroll_id=fields.Many2one('enroll.stud',string='Enrollment' ,domain=['|',('state','=','draft'),('state','=','new')])
    student_id=fields.Many2one('student.library',string='Enrollment')
    reasons=fields.Text(string="Reasons")
    cancel_date=fields.Date(string="Cancel date")
    
    
    
    # @api.model 
    # def default_get(self,fields):
    #     _logger.info("default is really????????????????????????????????????????")
    #     res=super(CancelsIssue,self).default_get(fields)
    #     res['cancel_date']=datetime.date.today()
    #     res['enroll_id']=self.env.context.get('active_id')
    #     return res
    
  
    
    
    
    def action_cancel(self):
        cancel_days=self.env['ir.config_parameter'].get_param('rg_library.cancel_days')
        allowed_date=date.today() - relativedelta.relativedelta(days=int(cancel_days))
        if self.cancel_date > allowed_date: 
            raise ValidationError(("Same  cancelation not allowed"))
            
        
        # if self.enroll_id.joining_date == fields.Date.today():
        # return
    
    
    