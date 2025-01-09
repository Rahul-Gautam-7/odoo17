from odoo import fields,models 

class ResConfigSetting(models.TransientModel):
    _inherit="res.config.settings"
    
    cancel_time=fields.Integer(string="CancelTime",config_parameter='gaming.field')