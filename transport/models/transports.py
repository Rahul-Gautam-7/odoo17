from odoo import fields,models,api 


class TransportMod(models.Model):
    _name="trans.module"
    _description="It is transport module"
    _inherit=['mail.thread','mail.activity.mixin']
    
    name = fields.Char(string="Name",tracking=True)
    numbers=fields.Integer(string="Number_Plate",tracking=True)
    brand=fields.Char(string="CompanyBrand",tracking=True)
    active=fields.Boolean(string="active",tracking=True)
  