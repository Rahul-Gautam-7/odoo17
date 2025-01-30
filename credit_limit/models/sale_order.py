from odoo import api,fields,models
from odoo.exceptions import UserError
import logging

_logger = logging.getLogger(__name__)

class SaleOrder(models.Model):
    _inherit="sale.order"
    
    credit_limit = fields.Float(related='partner_id.credit_limit', string="Credit Limit",readonly=False)
    partner_hold = fields.Boolean(related='partner_id.hold', string="Hold Limit", readonly=False)
    
  
    def action_confirm(self):     
        for order in self:
                current_quote = sum(x.price_total for x in order.order_line)
                _logger.info(f"current_quote..................{current_quote}")
                _logger.info(order.partner_id.sale_order_count)
                previous_orders = self.env['sale.order'].search([
                    ('partner_id', '=', order.partner_id.id),
                ])
                _logger.info(previous_orders)
                if len(previous_orders) <= 1:
                    _logger.info("This is the customer's first order.")
                    return super(SaleOrder,self).action_confirm()
                else:
                    if order.partner_id.hold:
                        raise UserError("You Cannot Confirm your order as it is in hold state") 
                    if order.partner_id.check_limit:
                            popup=self.env['wizard.popup'].create({
                                'partner_id':order.partner_id.id,
                                'current_quotation':current_quote,
                                'msg':'credit exceeded'})
                            _logger.info("popup data %s",popup)
                            if popup.exceeding_amount>0:
                                _logger.info(popup.exceeding_amount)
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
  
    

                    
        