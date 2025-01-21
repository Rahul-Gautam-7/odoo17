from odoo import api,fields,models,_

class SaleReport(models.Model):
    _inherit='sale.report'
    
    confirm_user_id = fields.Many2one('res.users',string="Confirmed users",readonly=True)
    
    def _select_additional_fields(self):
        res = super()._select_additional_fields()
        res['confirm_user_id'] = f"""s.confirm_user_id"""
        return res