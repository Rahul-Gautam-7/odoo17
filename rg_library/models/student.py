from odoo import api, fields, models
from datetime import date
import logging 
from odoo.exceptions import ValidationError

_logger=logging.getLogger(__name__)

class StudentLibrary(models.Model):
    _name = 'student.library'
    _inherit=['mail.thread','mail.activity.mixin']
    _description = 'student Tag'
    
    name=fields.Char(string="Name",tracking=True)
    dob=fields.Date(string='DOB')
    age=fields.Integer(string="Age",compute='_compute_age',tracking=True)
    ref=fields.Char(string='reference',help="reference of student")
    gender=fields.Selection([('male','Male'),('female','Female')],string='Gender',tracking=True)
    active=fields.Boolean(string="Active")
    details=fields.Html(string='details')
    image=fields.Image(string="Image")
    enrollment_count=fields.Integer(string="Enroll Count" ,compute='_compute_enrollment_count', store=True)
    
    student_ids=fields.One2many('enroll.stud','student_id',string="Student")
    
    parent=fields.Char(string="parent")
    branch=fields.Selection([('bca','BCA'),('mca','MCA')], string="Branch", tracking=True)
    branch_name=fields.Char(string="BranchName")
    
    
    def action_t(self):
        _logger.info("Click success")
        return
    
    @api.depends('student_ids')
    def _compute_enrollment_count(self):
        for rec in self:
            rec.enrollment_count=self.env['enroll.stud'].search_count([('student_id','=',rec.id)])
    
    
    @api.ondelete(at_uninstall=False)
    def _check_enrollment_count(self):
            for rec in self:
                if rec.student_ids:
                    raise ValidationError("You cannot delete the student with enrollment")
    
    
    # @api.model
    # def create(self,vals):
    #     _logger.info(vals)
    #     vals['ref']=99
    #     record = super(StudentLibrary, self).create(vals)
    #     _logger.info(vals)
    #     return record
    
    def _compute_display_name(self):
        for x in self:
            x.display_name = f'{x.ref} {x.name}'
    
    
    @api.constrains('dob')
    def _check_dob(self):
        for rec in self:
            if rec.dob and rec.dob > fields.Date.today():
                raise ValidationError(("Enter a valid date"))
        
    
    @api.model 
    def create(self,vals):
        _logger.info(self.env['ir.sequence'])
        vals['ref']=self.env['ir.sequence'].next_by_code('rg_lib')
        record=super(StudentLibrary,self).create(vals)
        return record 
    
    def write(self, values):
        _logger.info("Written success")
        return super(StudentLibrary,self).write(values)
    
    
    @api.depends('dob')
    def _compute_age(self):
        for rec in self:
            today=date.today()
            if rec.dob:
                rec.age=today.year - rec.dob.year
            else:
                rec.age=0  
   
    
   