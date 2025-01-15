from odoo import api, fields, models,_
from datetime import date
import logging 
from odoo.exceptions import ValidationError
from dateutil import relativedelta

_logger=logging.getLogger(__name__)

class StudentLibrary(models.Model):
    _name = 'student.library'
    _inherit=['mail.thread','mail.activity.mixin']
    _description = 'student Tag'
    
    name=fields.Char(string="Name",tracking=True)
    dob=fields.Date(string='DOB')
    age=fields.Integer(string="Age",compute='_compute_age',search="_search_age",inverse="_inverse_compute_age",tracking=True)
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
    is_birthday=fields.Boolean(string="Birthday",compute="_chekc_bir")
    phone=fields.Char(string="Phone")
    email=fields.Char(string="Email")
    website=fields.Char(string="Website")
    
    
    def action_t(self):
        _logger.info("Click success")
        return
    
    @api.depends('student_ids')
    def _compute_enrollment_count(self):
        # for rec in self:
        #     rec.enrollment_count=self.env['enroll.stud'].search_count([('student_id','=',rec.id)])
            enrollment_group=self.env['enroll.stud'].read_group(domain=[('state','=','done')],fields=['student_id'],groupby=['student_id'])
            _logger.info(enrollment_group)
            print(enrollment_group)
            for x in enrollment_group:
                student_id=x.get('student_id')[0]
                student_rec=self.browse(student_id)
                student_rec.enrollment_count = x['student_id_count']
            self.enrollment_count=0
    

    
    
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
    
    @api.depends('age')
    def _inverse_compute_age(self):
       today = date.today()
       for rec in self:
           rec.dob= today - relativedelta.relativedelta(years=rec.age)
    
    @api.depends('dob')
    def _chekc_bir(self):
        for rec in self:
            is_birthday=False 
            if rec.dob: 
                today=date.today()
                _logger.info(today)
                if today.day == rec.dob.day and today.month == rec.dob.month:
                    is_birthday=True 
            rec.is_birthday=is_birthday
    
    @api.depends('dob')
    def _compute_age(self):
        for rec in self:
            today=date.today()
            if rec.dob:
                rec.age=today.year - rec.dob.year
            else:
                rec.age=0  
   
    def action_view_studentss(self):
        return{
            'name':_('Enrollments'),
            'res_model':'enroll.stud',
            'view_mode':'list,form,calendar,activity',
            'context':{'default_student_id':self.id},
            'domain':[('student_id','=',self.id)],
            'target':'current',
            'type':'ir.actions.act_window',
        }
    
    def _search_age(self,operator,value):
        dob=date.today() - relativedelta.relativedelta(years=value)
        start=dob.replace(day=1,month=1)
        endsy=dob.replace(day=31,month=12)
        return [('dob','>=',start),('dob','<=',endsy)]
        
    