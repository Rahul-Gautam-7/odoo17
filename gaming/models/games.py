from odoo import api, fields,models
import logging
from odoo.exceptions import ValidationError

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
    gm_count=fields.Integer(string="Game_count" ,compute="_compute_gm_count" , store=True)
    
    game_ids=fields.One2many('gm.game','game_id',string="GameCounts")
    
    @api.depends('game_ids')
    def _compute_gm_count(self):
        for rec in self:
            rec.gm_count=self.env['gm.game'].search_count([('game_id','=',rec.id)])
    
    @api.constrains('year')
    def _check_year(self):
        for rec in self:
            if rec.year and rec.year > 2025 :
                raise ValidationError(("Enter valid year"))                
        
   
    def create(self,vals):
        _logger.info(vals)
        vals['ref']=self.env['ir.sequence'].next_by_code('gamess')
        record=super(GameDev,self).create(vals)
        return record
    
    def _compute_display_name(self):
        for x in self:
            x.display_name=f'{x.ref}{x.name}'