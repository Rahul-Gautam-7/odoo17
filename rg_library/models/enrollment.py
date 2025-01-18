from odoo import models, fields,api,_ 
import logging 
from odoo.exceptions import ValidationError
import random

_logger=logging.getLogger(__name__)

class EnrollStud(models.Model):
    _name = 'enroll.stud'
    _description = 'Student Enrollment'
    _inherit=['mail.thread','mail.activity.mixin']
    _rec_name='student_id'
    _order='id desc'
    
    student_id=fields.Many2one('student.library',string="Student" ,ondelete='restrict',tracking=1)
    joining_time=fields.Datetime(string="Joining Time",default=fields.Datetime.now)
    joining_date=fields.Date(string="Joining Date",default=fields.Date.context_today,tracking=2)
    gender=fields.Selection(related="student_id.gender",readonly=False,tracking=5)
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
    detail=fields.Html(string="detail",tracking=4)
    hide_price=fields.Boolean(string="Hide Price")
    image=fields.Image(string="Image")
    tag_ids=fields.Many2many("student.tag",string="Tags")
    operation_name=fields.Many2one("lib.operation",string="Operation")
    progress=fields.Integer(string="Progress",compute="_progress_make")
    
    company_id=fields.Many2one('res.company',string="Company",default=lambda self:self.env.company)
    currency_id=fields.Many2one('res.currency',related='company_id.currency_id')
    
    total=fields.Float(string="Totals",compute="_total_c",store=True)
    
    @api.depends('book_line_ids.price_subtotal')
    def _total_c(self):
        for x in self:
            x.total=sum(rec.price_subtotal for rec in x.book_line_ids)
    
    
    def action_wp(self):
        message='hi %s ,your enrollment number is %s,Thank you'%(self.student_id.name,self.ref)
        whatsapp_url='https://api.whatsapp.com/send?phone=%s&text=%s'%(self.student_id.phone,message)
        return{
            'type':'ir.actions.act_url',
            'target':'new',
            'url':whatsapp_url
        }
    
    
    
    @api.depends('state')
    def _progress_make(self):
        for rec in self:
            if rec.state=='new':
                progress=random.randrange(0,25)
            elif rec.state=='draft':
                progress=random.randrange(26,85)
            elif rec.state == 'done':
                progress=100
            else:
                progress=0
            rec.progress=progress 
 
    
        
    
    
    @api.model 
    def create(self,vals): 
        vals['pro_ref']=self.env['ir.sequence'].next_by_code('proseq')
        record=super(EnrollStud,self).create(vals)
        return record
    
    # def unlink(self):
    #     if self.state == 'done':
    #         raise ValidationError(_("You cannot delete the done record state"))
    #     return super(EnrollStud,self).unlink()
    
    
    @api.onchange('student_id')
    def onchange_student_id(self):
        self.ref=self.student_id.ref
        
    def action_test(self):
        _logger.info("object button clicked")
        return{
            'type':'ir.actions.act_url',
            'target':'new',
            'url':'https://www.youtube.com'
        }
        
    
    def action_notification(self):
        action=self.env.ref('rg_library.student_form')
        return{
            'type':'ir.actions.client',
            'tag':'display_notification',
            'params':{
                'title':_('Click to continue'),
                'message':'%s',
                'links':[{
                    'label':self.student_id.name,
                    'url':f'#action={action.id}&id={self.student_id.id}&model=student.library',
                }],
                'sticky':False,
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
        return {
            'effect':{
                'fadeout':'slow',
                'message':'Click Success',
                'type':'rainbow_man'
            }
        }
            
    
    def _compute_display_name(self):
        for x in self:
            x.display_name = f'{x.pro_ref}'
    
       
       
class BooksST(models.Model):
    _name="books"
    _description="book models"
    
    
    
    product_id=fields.Many2one('product.product',required=True)
    price=fields.Float(related='product_id.lst_price',readonly=False,digits='Product Price')
    qty=fields.Integer(string="Quantity",default="1")
    book_id=fields.Many2one('enroll.stud',string="Books")
    
    currency_id=fields.Many2one('res.currency',related='book_id.currency_id')
    price_subtotal=fields.Monetary(string="SubTotal",compute="_compute_price_subtotal",currency_field='currency_id')
    
    @api.depends('price','qty')
    def _compute_price_subtotal(self):
        for rec in self:
            rec.price_subtotal=rec.price *rec.qty