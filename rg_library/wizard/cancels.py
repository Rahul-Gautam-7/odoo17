from odoo import models,api,fields 
import logging 
import datetime 
from odoo.exceptions import ValidationError

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
        if self.enroll_id.joining_date == fields.Date.today():
            raise ValidationError(("Same date cancelation not allowed"))
        return
    
    