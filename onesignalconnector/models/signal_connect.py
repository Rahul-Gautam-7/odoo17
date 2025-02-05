from odoo import api,fields,models
import requests
import logging

_logger = logging.getLogger(__name__)

class SignalConnect(models.Model):
    _name="signal.connect"
    _description="Signal connection model"
    
    
    name=fields.Char(string="Connector Name",required=True)
    app_id=fields.Char(string="App ID",required=True)
    api_key=fields.Char(string="Api Key",required=True)
    status=fields.Selection([
        ('connected','Connected'),
        ('disconnected','Disconnected'),
    ],readonly=True,default="disconnected")
    
    total_players=fields.Integer(string="Total Players",compute="_compute_total")
    
    
    def action_connect(self):
        self.ensure_one()
        url=f"https://api.onesignal.com/apps/{self.app_id}"
        headers={
            "Authorization" : f"Basic {self.api_key}",
            "Content-Type":"application/json"
        }
        try:  
            response = requests.get(url,headers=headers)
        
            if response.status_code == 200:
                self.status='connected'
                _logger.info("Connection Success")
            else:
                self.status='disconnected'
                _logger.info(response.text)
                
        except requests.exceptions.RequestException as e:
            self.status = 'disconnected'
            _logger.error("Connection Failed: %s", str(e))  
        return True
    
    def action_sync_user(self):
        self.ensure_one()
        user_fetch=self.env['user.fetch']
        user_fetch.check_users()
        _logger.info("Fetch Success")
        self._compute_total()
        return True
    
    def action_sync_segments(self):
        self.ensure_one()
        seg_fetch=self.env['onesignal.segment']
        seg_fetch.check_segments()
        _logger.info("Segment Sync Success")
        return True
    
    def action_sync_templates(self):
        self.ensure_one()
        temp_fetch=self.env['onesignal.template']
        temp_fetch.check_templates()
        _logger.info("Template Sync Success")
        return True
    
    def _compute_total(self):
        for record in self:
            player_count = self.env['user.fetch'].search_count([('connector_ids','=',record.id)])
            _logger.info("Record Success")
            record.total_players = player_count
            _logger.info(record.total_players)
        
 
        
    
    
            