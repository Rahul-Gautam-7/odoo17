from odoo import api,fields,models 
import logging 
from datetime import date
from dateutil import relativedelta
from odoo.exceptions import ValidationError

_logger=logging.getLogger(__name__)

class Cancels(models.TransientModel):
    _name="cancel.game"
    _description="Cancel games"
    
    gnm_id=fields.Many2one('gm.game',string="GM",domain=['|',('state','=','draft'),('state','=','new')] )
    @api.model 
    def default_get(self,fields):
        _logger.info("working right????????????????????????????????????")
        res=super(Cancels,self).default_get(fields)
        res['delay_date']=date.today()
        res['gnm_id']=self.env.context.get('active_id')
        return res
    
    # game_id=fields.Many2one('game.industry',String="Games")
    reasons=fields.Text(string="reasons")
    delay_date=fields.Date(string="Delay date")
    
        
    def action_cancels(self):
        # if self.gnm_id.game_date == fields.Date.today():
        cancel_day=self.env['ir.config_parameter'].get_param('gaming.field')
        allowed_day=date.today()-relativedelta.relativedelta(days=int(cancel_day))
        if self.delay_date > allowed_day:
            raise ValidationError(("Delay must be before or on",allowed_day))
        return
    
  
        