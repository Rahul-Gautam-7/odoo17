from odoo import api,fields,models

class ResConfigSettings(models.TransientModel):
    _inherit="res.config.settings"
    
    min_stock=fields.Integer(string="Minimum Stocks",config_parameter="low_stock_notification.min_stock")