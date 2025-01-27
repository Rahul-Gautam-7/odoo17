from odoo import models,fields,api

class LowStockNotification(models.Model):
    _name="low.stock.notification"
    _description="module to notify when low stock"
    
    
    
    name=fields.Char(string="Low value notify")
    product_ids=fields.Many2one('product.product',string="Low Stock Products")
    
    
    @api.model
    def notify_low_stock(self):
        min_stock_str=self.env['ir.config_parameter'].get_param('low_stock_notification.min_stock')
        
        try:
            min_stock = int(min_stock_str)
        except ValueError:
            min_stock = 10 
        
        low_stock_product=self.env['product.product'].search([('qty_available','<',min_stock)])
        low_pro_list=[]
        products_to_remove = []
        
        # Checking the existing product in the list
        
        for product in low_stock_product:
            existing_product = self.env['low.stock.product'].search([
                ('product_name', '=', product.name),
                ('notification_id', '=', self.id)
            ], limit=1)

            if not existing_product:  
                low_pro_list.append({
                    'product_name': product.name,
                    'stock': product.qty_available,
                })
            else:
                if existing_product.stock != product.qty_available:
                    existing_product.write({
                        'stock':product.qty_available,
                    })

        
        
        # if the stock qty increases from the minimum stock so we remove from list
        
        for product in self.env['low.stock.product'].search([('notification_id', '=', self.id)]):
            product_record = self.env['product.product'].search([('name', '=', product.product_name)], limit=1)
        
            if product_record and product_record.qty_available >= min_stock:
           
                products_to_remove.append(product)

        for product in products_to_remove:
            product.unlink()


        # appending the value of the low stock products in the list
        
        if low_pro_list:
            self.env['low.stock.product'].create([{
                'product_name': rec['product_name'],
                'stock': rec['stock'],
                'notification_id': self.id,
            } for rec in low_pro_list])

        return True
