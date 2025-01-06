from odoo import api, fields,models
import logging

_logger=logging.getLogger(__name__)

class GameDev(models.Model):
    _name="game.industry"
    _inherit=['mail.thread','mail.activity.mixin']
    _description="List of games"
    
    name = fields.Char(string="Game Name",tracking=True)
    year = fields.Integer(string="Year",tracking=True)
    active=fields.Boolean(string="Active")
    ref=fields.Char(string='reference',help="reference for games")
    desc=fields.Html(string='desc')
   
    def create(self,vals):
        _logger.info(vals)
        vals['ref']=self.env['ir.sequence'].next_by_code('gamess')
        record=super(GameDev,self).create(vals)
        return record
    
    def _compute_display_name(self):
        for x in self:
            x.display_name=f'{x.ref}{x.name}'