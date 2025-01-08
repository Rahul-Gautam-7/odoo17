from odoo import api,fields,models 
import datetime 

class CNC(models.TransientModel):
    _name="cancelss"
    _description="This is cancel model"
   
    
    ors_id = fields.Many2one('prs',string="Order")
    reason = fields.Text(string="Reason")
    cancel_date = fields.Date(string="Date")
    
   
    
    @api.model 
    def default_get(self,fields):
        res = super(CNC,self).default_get(fields)
        res['ors_id'] = self.env.context.get('active_id')
        return res
    