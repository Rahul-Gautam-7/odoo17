from odoo import models, fields,api,_ 
import logging 
from odoo.exceptions import ValidationError

_logger=logging.getLogger(__name__)

class EnrollStud(models.Model):
    _name = 'enroll.stud'
    _description = 'Student Enrollment'
    _inherit=['mail.thread','mail.activity.mixin']
    _rec_name='student_id'
    
    student_id=fields.Many2one('student.library',string="Student" ,ondelete='restrict')
    joining_time=fields.Datetime(string="Joining Time",default=fields.Datetime.now)
    joining_date=fields.Date(string="Joining Date",default=fields.Date.context_today)
    gender=fields.Selection(related="student_id.gender",readonly=False)
    #ref=fields.Integer(related="student_id.ref")  
    pro_ref=fields.Char(string="productref" ,readonly=True)
    ref=fields.Char(string="reference")
    priority=fields.Selection([
        ('0','normal'),
        ('1','medium'),
        ('2','high')
    ],string='priority')
    state=fields.Selection([
        ('new','New'),
        ('draft','Draft'),
        ('done','Done'),
        ('cancel','Cancel'),
    ],string='status',default='new')
    librarian_id=fields.Many2one('res.users',string="Librarian")
    book_line_ids=fields.One2many('books','book_id',string="Books Lines")
    detail=fields.Html(string="detail")
    hide_price=fields.Boolean(string="Hide Price")
    image=fields.Image(string="Image")
    tag_ids=fields.Many2many("student.tag",string="Tags")
    
    
    
    @api.model 
    def create(self,vals): 
        vals['pro_ref']=self.env['ir.sequence'].next_by_code('proseq')
        record=super(EnrollStud,self).create(vals)
        return record
    
    def unlink(self):
        if self.state == 'done':
            raise ValidationError(_("You cannot delete the done record state"))
        return super(EnrollStud,self).unlink()
    
    
    @api.onchange('student_id')
    def onchange_student_id(self):
        self.ref=self.student_id.ref
        
    def action_test(self):
        _logger.info("object button clicked")
        return {
            'effect':{
                'fadeout':'slow',
                'message':'Click Success',
                'type':'rainbow_man'
            }
        }
    
    def action_draft(self):
        for x in self:
            x.state='draft'
    
    def action_cancel(self):
        # action=self.env.ref('rg_library.action_cancel_is').read()[0]
        for x in self:
            x.state='cancel'
        
        
    def action_done(self):
        for x in self:
            x.state='done'
            
    
    def _compute_display_name(self):
        for x in self:
            x.display_name = f'{x.pro_ref}'
    
       
       
class BooksST(models.Model):
    _name="books"
    _description="book models"
    
    
    
    product_id=fields.Many2one('product.product',required=True)
    price=fields.Float(related='product_id.lst_price',readonly=False)
    qty=fields.Integer(string="Quantity",default="1")
    book_id=fields.Many2one('enroll.stud',string="Books")