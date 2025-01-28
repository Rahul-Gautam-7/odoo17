from odoo import api,fields,models
from odoo.exceptions import UserError


class SaleOrder(models.Model):
    _inherit="sale.order"
    
    credit_limit = fields.Float(related='partner_id.credit_limit', string="Credit Limit",readonly=False)
    partner_hold = fields.Boolean(related='partner_id.hold', string="Hold Limit", readonly=False)
            
    def action_confirm(self):     
        for order in self:
                if order.partner_id.hold:
                    raise UserError("You Cannot Confirm your order as it is in hold state") 
                if order.partner_id.check_limit:
                    popup= self.env['wizard.popup'].create({
                        'partner_id':order.partner_id.id,
                        'msg':'credit exceeded',
                    })
                    if popup.exceeding_amount > 0:
                        return{
                            'name':'Credit Limit Warning',
                            'view_type':'form',
                            'view_mode':'form',
                            'res_model':'wizard.popup',
                            'type':'ir.actions.act_window',
                            'target':'new',
                            'res_id':popup.id,
                        }
        return super(SaleOrder,self).action_confirm()