from odoo import api,fields,models
import logging

_logger = logging.getLogger(__name__)

class WizardPopup(models.TransientModel):
    _name="wizard.popup"
    _description="A Popup during confirmation"
    
    partner_id=fields.Many2one('res.partner',string="Customer")
    msg=fields.Char(string="message",readonly=True,default="Credit Limit Exceeded")
    check_limit = fields.Boolean(related='partner_id.check_limit', string="Check Limit",readonly=False)
    credit_limit = fields.Float(related='partner_id.credit_limit', string="Credit Limit",readonly=False)
    hold = fields.Boolean(related='partner_id.hold', string="Hold",readonly=False)
    
    # # calulations
    total_receivable=fields.Monetary(string="Total Receivable",compute="_compute_total_receivable")
    sales_order=fields.Monetary(string="Sales Order",compute="_compute_sales_order")
    invoices=fields.Monetary(string="invoices",compute="_compute_invoices")
    current_quotation=fields.Float(string="Current Quotation")  
    exceeding_amount=fields.Float(string="Exceeded Amount",compute="_compute_exceeding_amount")
      
    currency_id = fields.Many2one('res.currency', string="Currency", related='partner_id.currency_id', store=True)
    
    
    sale_order_id=fields.Many2one('sale.order',string="Sale Order")
    
    @api.depends('partner_id')
    def _compute_total_receivable(self):
        for wiz in self:
            receivable=0
            invoices=self.env['account.move'].search([
                ('partner_id','=',wiz.partner_id.id),
                ('state','=','posted'),
                ('amount_residual', '>', 0) 
            ])
            receivable=sum(invoice.amount_total for invoice in invoices)
            wiz.total_receivable=receivable
            
    def _compute_sales_order(self): 
        for record in self:
            # add draft orders
            pending_orders = self.env['sale.order'].search([
                ('partner_id','=',record.partner_id.id),
                ('state', 'in', ['draft','sale'])
            ])
            amt = sum(order.amount_total for order in pending_orders)
            invoice=sum(o.amount_invoiced for o in pending_orders)
            _logger.info(f"invoice...................{invoice}")
            if record.current_quotation:
                record.sales_order =round(amt - record.current_quotation - invoice, 3)
            else:
                record.sales_order =round(amt - invoice, 3)
        
    
    @api.depends('current_quotation')
    def _compute_invoices(self):
        for wiz in self:
            _logger.info("current_quotation %s",wiz.current_quotation)
            draft_invo=0
            d_invoices=self.env['account.move'].search([
                ('partner_id','=',wiz.partner_id.id),
                ('state','=','draft'),
            ])
            draft_invo=sum(invoice.amount_total for invoice in d_invoices)
            wiz.invoices=draft_invo
                       
    @api.depends('total_receivable', 'sales_order', 'invoices', 'current_quotation', 'credit_limit')
    def _compute_exceeding_amount(self):
        for wiz in self:
            total=(wiz.total_receivable + wiz.sales_order + wiz.invoices + wiz.current_quotation )
            wiz.exceeding_amount=total - wiz.credit_limit
            _logger.info("total_receivable %s",wiz.total_receivable)
            _logger.info("sales_order %s",wiz.sales_order)
            _logger.info("invoices %s",wiz.invoices)
            _logger.info("current_quotation %s",wiz.current_quotation)
            _logger.info("exceeding_amount %s",wiz.exceeding_amount)


    
    def set_partner_hold(self):
        if self.sale_order_id:
            partner = self.sale_order_id.partner_id
            if partner:
                partner.write({'hold': True})    
