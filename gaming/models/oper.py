from odoo import fields,api,models 

class OPR(models.Model):
    _name="operationss"
    _description="Just operations related to gaming"
    _log_access=False
    # _rec_name="gname"
    _order="sequence,id"
    
    
    gname=fields.Char(string="GNAMe")
    g_id=fields.Many2one('res.users',string="Gamers")
    references=fields.Reference(selection=[('game.industry','Gamers'),('gm.game','PCVR')],string="Refer")
    
    sequence=fields.Integer(string="Sequence")
    
    
    @api.model 
    def name_create(self,name):
        return self.create({'gname':name}).name_get()[0]