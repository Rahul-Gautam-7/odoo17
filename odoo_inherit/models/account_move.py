from odoo import models, fields, api


class AccountMove(models.Model):
    _inherit = 'account.move'
    _description = 'odoo_inherit.accountmove'

    so_confirm_user_id = fields.Many2one('res.users',string="SoConfirm")
    
    
    

 
class AccountMoveLine(models.Model):
    _inherit = 'account.move.line'
    _description = 'odoo_inherit.accountmoveline'

    line_number=fields.Integer(string="lineNumber")