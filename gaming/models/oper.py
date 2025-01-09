from odoo import fields,api,models 

class OPR(models.Model):
    _name="operationss"
    _description="Just operations related to gaming"
    _log_access=False
    # _rec_name="gname"
    
    
    gname=fields.Char(string="GNAMe")
    g_id=fields.Many2one('res.users',string="Gamers")
    
    
    
    @api.model 
    def name_create(self,name):
        return self.create({'gname':name}).name_get()[0]