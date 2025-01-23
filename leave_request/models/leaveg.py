from odoo import models,api,fields
from datetime import date

class LeaveRequest(models.Model):
    _name="hr.leave.request"
    _description="Leave request model"
    _rec_name='employee_id'
    
    employee_id=fields.Many2one('hr.employee',string="Employee")
    leave_type=fields.Selection([('unpaid','Unpaid'),('paid','Paid'),('sickleave','Sickleave')],string="LeaveType")
    start_date=fields.Date(string="StartDate")
    end_date=fields.Date(string="EndDate")
    reason=fields.Char(string="Reason")
    status=fields.Selection([
        ('draft','Draft'),
        ('pending','Pending'),
        ('approved','Approved'),
        ('rejected','Rejected'),
    ],default='draft')
 
    
    
    def action_approved(self):
        self.status='approved'
        return
    
    def action_reject(self):
        self.status='rejected'
        return
    
    def action_confirm(self):
        self.status='pending'
        return