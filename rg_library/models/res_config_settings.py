from odoo import fields,models 

class ResConfigSettings(models.TransientModel):
    _inherit="res.config.settings"
    
    cancel_days=fields.Integer(string="Cancel Days",config_parameter='rg_library.cancel_days')