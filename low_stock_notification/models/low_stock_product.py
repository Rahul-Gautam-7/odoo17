from odoo import api,fields,models


class LowStockProduct(models.Model):
    _name="low.stock.product"
    _description="Low stock products"
    
    product_name=fields.Char(string="ProductName")
    stock=fields.Float(string="Remaining Stock")
    notification_id=fields.Many2one('low.stock.notification',string="Notify")