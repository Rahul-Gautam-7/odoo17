from odoo import models,api,fields

class LSP(models.Model):
    _name="l.s.p"
    _description="test purpose"
    
    product_ids=fields.Many2one('product.template',string="Products")
    
    
    @api.model
    def lowsp(self):
        min_stock=5
        add_pro=[]
        remove_pro=[]
        
        low_pro_list=self.env['product.template'].search([('qty_available','<',min_stock)])
        
        # first step to verify that the product is not existing
        for product in low_pro_list:
            exist_pro=self.env['bind.mod'].search([
                ('product_name','=',product.name),
                ('bind_field_id','=',self.id),
            ],limit=1)
            
            if not exist_pro:
                add_pro.append({
                    'product_name':product.name,
                    'stk':product.qty_available,
                })
            else : 
                if exist_pro.stk != product.qty_available:
                    exist_pro.write({
                        'stk':product.qty_available,
                    })
                    
                    
        # second step to remove if the quantity increases from minimum stock
        for product in self.env['bind.mod'].search([('bind_field_id','=',self.id)]):
            pro_rec=self.env['product.template'].search([('name','=',product.product_name)],limit=1)
            
            if pro_rec and pro_rec.qty_available >= min_stock:
                remove_pro.append(product)
        
        for product in remove_pro:
            product.unlink()
            
        
        # Third and final step is to add the field in the list
        if add_pro:
            self.env['bind.mod'].create([{
                'product_name':rec['product_name'],
                'stk':rec['stk'],
                'bind_field_id':self.id,
            }for rec in add_pro])
            
        return True
            