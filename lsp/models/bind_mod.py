from odoo import api,fields,models

class BINDMOD(models.Model):
    _name="bind.mod"
    _description="binded model for list view"
    
    product_name=fields.Char(string="Product Name")
    stk=fields.Integer(string="Stock QTY")
    bind_field_id=fields.Many2one('l.s.p',string="Binded Field")