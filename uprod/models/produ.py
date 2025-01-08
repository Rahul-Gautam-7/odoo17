from odoo import api,fields,models 
from odoo.exceptions import ValidationError

class Prod(models.Model):
    _name="prods"
    _description="product related"
    
    
    # _sql_constraints =[
    #     ('unique_pro_name','unique(name)','Must be unique name of products'),  
    # ]
    
    name=fields.Char(string='Name' ,tracking=True)
    ref=fields.Char(string='Product_ID', tracking=True)
    category=fields.Selection([
        ('cons','Consumable'),
        ('stor','Storable'),
        ('combo','Combo'),
        ('serv','Service'),
    ],string='Category', tracking=True)
    price=fields.Integer(string='Price', tracking=True)
    active=fields.Boolean(string='Active', tracking=True)
    
    @api.constrains('price')
    def _check_price(self):
        for rec in self:
            if rec.price and rec.price < 0:
                raise ValidationError(("Enter valid price"))
    
    
    def create(self,vals):
        vals['ref'] = self.env['ir.sequence'].next_by_code('prose')
        record = super(Prod,self).create(vals)
        return record 
    
     
    
    