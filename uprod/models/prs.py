from odoo import api,models ,fields 
from datetime import date,timedelta
from dateutil.relativedelta import relativedelta

class PRSS(models.Model):
    _name="prs"
    _description="Detailed products"
    _inherit=['mail.thread','mail.activity.mixin']
    _rec_name='prs_id'
    
    
    prs_id=fields.Many2one('prods',string="Products",tracking=True)
    quantity=fields.Integer(string="Quantity" ,tracking=True)
    mfg_date=fields.Date(string="ManuFactured Date")
    exp_date=fields.Date(string="Expiry Date",readonly=True)
    seller_id=fields.Many2one('res.users',string="Sellers")
    ref=fields.Char(related="prs_id.ref", tracking=True)
    priority=fields.Selection([
        ('1','low'),
        ('2','medium'),
        ('3','high'),
        ('4','veryhigh'),
    ],string="priority")
    state=fields.Selection([
        ('new','New'),
        ('draft','Draft'),
        ('done','Done'),
        ('cancel','Cancel'),
    ],string="states",default="new")
    details=fields.Html(string="detatils")
    
    @api.onchange('mfg_date')
    def _years(self):
        for x in self:
            today=date.today()
            if x.mfg_date:
                x.exp_date=today+timedelta(5*365)
            else:
                x.exp_date=False
    
    def action_draft(self):
        for x in self:
            x.state='draft'
    
    def action_done(self):
        for x in self:
            x.state='done'
            return {
            'effect':{
                'fadeout':'slow',
                'message':"order confirm",
                'type':'rainbow_man'
            }
        }
    
    def action_cancel(self):
        for x in self:
            x.state='cancel'