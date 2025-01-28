from odoo import api,fields,models

class CredLim(models.Model):
    _inherit = 'res.partner'
    _description = "Sale order for custom field"
    
    
    check_limit=fields.Boolean(string="Check Limit")
    credit_limit=fields.Float(string="Credit Limit")
    hold=fields.Boolean(string="Hold Limit")