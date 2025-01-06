from odoo import fields,models,api 
from datetime import date
from dateutil.relativedelta import relativedelta

class Test(models.Model):
    _name="test.mode"
    _description="Test model in transport"
    
    test_id=fields.Many2one('trans.module',string='name')
    numbers=fields.Integer(related='test_id.numbers')
    reg_date=fields.Date(string="Registration Date",default=fields.Date.context_today)
    service=fields.Date(string="Service Date", compute="_services")
    state=fields.Selection([
        ('new','New'),
        ('draft','Draft'),
        ('done','Done'),   
    ],string="status",default='new')
    
    
    @api.depends('reg_date')
    def _services(self):
        for x in self:
            today=date.today()
            if x.reg_date:
                x.service = (today + relativedelta(years=5))
            else:
                x.service=today
            
        