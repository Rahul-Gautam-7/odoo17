from odoo import models, fields, api


class SaleOrder(models.Model):
    _inherit = 'sale.order'
    _description = 'odoo_inherit.odoo_inherit'

    confirm_user_id = fields.Many2one('res.users',string="Confirmed users")
    
    
    

    def action_confirm(self):
        super(SaleOrder,self).action_confirm()
        print("success")
        self.confirm_user_id=self.env.user.id

