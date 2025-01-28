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
    current_quotation=fields.Monetary(string="Current Quotation",compute="_compute_current_quotation")  
    exceeding_amount=fields.Monetary(string="Exceeded Amount",compute="_compute_exceeding_amount")
      
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
        for wiz in self:
            orders=0
            sale_order=self.env['sale.order'].search([
                ('partner_id','=',wiz.partner_id.id),
                ('state','in',['draft','sale','done']),
                ('date_order','<=',fields.Date.today()), 
            ],order='date_order desc')
            
            exclude_latest = sale_order[:1]  
            remaining_orders = sale_order[1:]  
            
            for value in remaining_orders:
                if not value.invoice_ids:
                    orders+= value.amount_total - value.amount_invoiced
                    
            wiz.sales_order=orders
        
    

    def _compute_invoices(self):
        for wiz in self:
            draft_invo=0
            d_invoices=self.env['account.move'].search([
                ('partner_id','=',wiz.partner_id.id),
                ('state','=','draft'),
            ])
            draft_invo=sum(invoice.amount_total for invoice in d_invoices)
            wiz.invoices=draft_invo
            
        
    @api.depends('sale_order_id')
    def _compute_current_quotation(self):
        for wiz in self:
            if wiz.sale_order_id:
                _logger.info(f"Computing for sale order: {wiz.sale_order_id.name}")
                wiz.current_quotation = sum(line.price_total for line in wiz.sale_order_id.order_line)
            else:
                _logger.info("No sale_order_id found, setting current_quotation to 0.")
                wiz.current_quotation = 0.0
            
    @api.depends('total_receivable', 'sales_order', 'invoices', 'current_quotation', 'credit_limit')
    def _compute_exceeding_amount(self):
        for wiz in self:
            total=(wiz.total_receivable + wiz.sales_order + wiz.invoices + wiz.current_quotation )
            wiz.exceeding_amount=total - wiz.credit_limit

    
    def set_partner_hold(self):
        if self.sale_order_id:
            partner = self.sale_order_id.partner_id
            if partner:
                partner.write({'hold': True})    
      