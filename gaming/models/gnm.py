from odoo import fields,models ,api , _ 
import logging
from odoo.exceptions import ValidationError

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
   
    @api.model 
    def create(self,vals):
        vals['order_ref']=self.env['ir.sequence'].next_by_code('or_ref')
        record=super(GNM,self).create(vals)
        return record
    
    def unlink(self):
        if self.state == 'done':
            raise ValidationError(_("Done state cannot be deleted"))
        return super(GNM,self).unlink()
            
        
        
    def objects_act(self):
        _logger.info("Object Clicked!!!!!!!!!!!!")
        return {
            'effect':{
                'fadeout':'slow',
                'message':'Its a rainbow',
                'type':'rainbow_man'
            }
        }
  
    
    
   
    
    def action_draft(self):
        for x in self:
            x.state='draft'
    
    def action_done(self):
        for x in self:
            x.state='done'
    
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