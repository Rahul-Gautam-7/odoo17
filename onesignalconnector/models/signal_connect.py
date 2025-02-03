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
    
    player_ids=fields.Text(string="Players IDs")
    notification_title=fields.Char(string="notification title",required=True)
    notification_message=fields.Text(string="notification message",required=True)
    
    
    
    
    def action_connect(self):
        
        url="https://onesignal.com/api/v1/apps"
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
    
    
    def send_push_notification(self):
        if not self.status=='connected':
            _logger.error("Connection Failure")
            return
        
        url= "https://onesignal.com/api/v1/notifications"
        headers={
            "Authorization":f"Basic {self.api_key}",
            "Content-Type":"application/json",
        }
        
        player_ids=self.player_ids.split(',')
        
        payload={
            "app_id":self.app_id,
            "include_player_ids":player_ids,
            "headings":{"en":self.notification_title},
            "contents":{"en":self.notification_message}
        }
        
        try:
            response=requests.post(url, json=payload, headers=headers)
            if response.status_code == 200:
                _logger.info("Push Notification Successs")
            else:
                _logger.error("Failed to push notify",response.text)
        except requests.exceptions.RequestException as e:
            _logger.info("Error in sending notifiy",str(e))
        
    