from odoo import api,fields, models

class PartnerCategory(models.Model):
    _name='res.partner.category'
    _inherit=['mail.thread','res.partner.category']
    
    name=fields.Char(tracking=True)