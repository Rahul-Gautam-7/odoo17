from odoo import fields,models ,api , _ 
import logging
from odoo.exceptions import ValidationError
import random 

_logger = logging.getLogger(__name__)

class GNM(models.Model):
    _name="gm.game"
    _description="Game extra"
    _inherit=['mail.thread','mail.activity.mixin']
    _rec_name="game_id"
    _order="id desc"
    
    game_id=fields.Many2one('game.industry',String="Games",ondelete="cascade")
    game_time=fields.Datetime(string="Game Time",default=fields.Datetime.now)
    game_date=fields.Date(string="Game Date",default=fields.Date.context_today)
    ref=fields.Char(related='game_id.ref')
    order_ref=fields.Char(string="Order Ref",readonly=True)
    priority=fields.Selection([
        ('0','normal'),
        ('1','medium'),
        ('2','high'),
    ],string="priority")
    state=fields.Selection([
        ('new','New'),
        ('draft','Draft'),
        ('done','Done'),
        ('cancel','Cancel')
    ],string="Status" ,default='new')
    gamers_id=fields.Many2one('res.users',string="Gamers")
    des=fields.Html(string='des')
    gms_game_ids=fields.One2many('gms','gms_id',string="Game lines")
    hide_price=fields.Boolean(string="Hide Price")
    img=fields.Image(string="image")
    tags_ids=fields.Many2many('tags',string="Tags")
    g_id=fields.Many2one('operationss',string="NewGamer")
    progress=fields.Integer(string="ProgressBar" , compute="_prog_compute")
    
    company_id=fields.Many2one('res.company',string="Company",default=lambda self:self.env.company)
    currency_id=fields.Many2one('res.currency',related="company_id.currency_id")
    
    
    total=fields.Float(string="total",compute="_compute_total")
    
    
    
    def action_wps(self):
        message="hi %s your reference is %s.ThankYOu"%(self.game_id.name,self.ref)
        whatspp_url="https://api.whatsapp.com/send?phone=%s&text=%s"%(self.game_id.phone,message)
        return{
            'type':'ir.actions.act_url',
            'target':'new',
            'url':whatspp_url
        }
    
    
    
    @api.depends('gms_game_ids.sub_total')
    def _compute_total(self):
        for x in self:
            x.total=sum(rec.sub_total for rec in x.gms_game_ids )
        
    
    
    
    
    @api.depends('state')
    def _prog_compute(self):
        for rec in self:
            if rec.state=='new':
                progress=random.randrange(0,40)
            elif rec.state=='draft':
                progress=random.randrange(41,80)
            elif rec.state=='done':
                progress=100
            else:
                progress=0
            rec.progress=progress
   
    @api.model 
    def create(self,vals):
        vals['order_ref']=self.env['ir.sequence'].next_by_code('or_ref')
        record=super(GNM,self).create(vals)
        return record
    
    # def unlink(self):
    #     if self.state == 'done':
    #         raise ValidationError(_("Done state cannot be deleted"))
    #     return super(GNM,self).unlink()
            
        
        
    def objects_act(self):
        _logger.info("Object Clicked!!!!!!!!!!!!")
        return{
            'type':'ir.actions.act_url',
            'target':'new',
            'url':'https://store.epicgames.com'
        }
        
  
    
    
   
    
    def action_draft(self):
        for x in self:
            x.state='draft'
    
    def action_done(self):
        for x in self:
            x.state='done'
        return {
            'effect':{
                'fadeout':'slow',
                'message':'Its a rainbow',
                'type':'rainbow_man'
            }
        }
    
    def action_cancel(self):
         #action=self.env.ref('gaming.action_cancel_gm').read()[0]
         for x in self:
            x.state='cancel' 
  
            
     
    def _compute_display_name(self):
        for x in self:
            x.display_name=f'{x.order_ref}'
    
    
class GMS(models.Model):
    _name="gms"
    _description="games models desc"
    
    product_id=fields.Many2one('product.product',string="product")
    price=fields.Float(related='product_id.lst_price')
    upt=fields.Integer(string="updates")
    gms_id=fields.Many2one('gm.game',string="gms")
    currency_id=fields.Many2one('res.currency',related="gms_id.currency_id")
    sub_total=fields.Monetary(string="subtotal",compute="_compute_total")
    
    @api.depends('upt','price')
    def _compute_total(self):
        for rec in self:
            rec.sub_total=rec.upt * rec.price 
            