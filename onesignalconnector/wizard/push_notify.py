from odoo import api,fields,models
import logging
import requests

_logger=logging.getLogger(__name__)

class PushNotify(models.TransientModel):
    _name="push.notify"
    _description="Wizard to notify"
    
    connector_ids=fields.Many2one('signal.connect',string="Onesignal AccountName")
    notification_type=fields.Selection([
        ('push','Push Notification'),
        ('email','Email Notification'),
        ('sms','SMS Notification')
    ],string="Notification Type")
    template=fields.Boolean(string="Using Template")
    heading=fields.Char(string="Heading")
    content=fields.Text(string="Content")
    cover_url=fields.Char(string="Cover URL")
    redirect_url=fields.Char(string="Redirect URL")
    action_btn=fields.Boolean(string="Action Button")
    send_to=fields.Selection([
        ('all',"All"),
        ('subscription_id','Subscription_ID')
    ],string="Send To")
    
    abc=fields.Char(string="Channel",compute="_compute_template_domain",default='push')
    
    template_id=fields.Many2one('onesignal.template',string='Template')
   

    
    # @api.depends('notification_type','connector_ids','template_id')
    # def _compute_template_domain(self):
    #     if self.notification_type == 'push' and self.connector_ids == self.template_id.connector_ids:
    #         self.abc = 'push' 
    #     elif self.notification_type == 'email':
    #         self.abc = 'email' 
    #     elif self.notification_type == 'sms':
    #         self.abc = 'sms' 
       
    @api.depends('notification_type', 'connector_ids', 'template_id')
    def _compute_template_domain(self):
        for record in self:
            if record.notification_type == 'push' and record.connector_ids and record.template_id and record.connector_ids == record.template_id.connector_ids:
                record.abc = 'push'
            elif record.notification_type == 'email':
                record.abc = 'email'
            elif record.notification_type == 'sms':
                record.abc = 'sms'
            else:
                record.abc = 'push'  # Default to push or handle as needed

  

            
            
        
    def action_send_notify(self):
        for record in self:
            app_id=record.connector_ids.app_id
            _logger.info(app_id)
            api_key=record.connector_ids.api_key
            
            if app_id:
                url="https://api.onesignal.com/notifications?c=push"
                
                payload={
                    "app_id":app_id,
                    "url":record.redirect_url,
                    "include_player_ids":[],
                    "template_id":record.template_id.temps_id 
                }
                if isinstance(self.content, str) and self.content.strip():
                    payload["contents"] = {"en": self.content}
                if isinstance(self.heading, str) and self.heading.strip():
                    payload["headings"] = {"en": self.heading}
                if record.send_to == 'all':
                    payload["included_segments"]=["All"]
                else:
                    _logger.info("Failed to send notification")
                    
                headers={
                    'Authorization':f"Basic {api_key}",
                    'Content-Type':'application/json',
                }
                
                try:
                    response=requests.post(url,json=payload,headers=headers)
                    _logger.info(response.text)
                    if response.status_code == 200:
                        _logger.info(f"Notification Sent Success : {response.text} ")
                    else:
                        _logger.info(response.status_code)
                except Exception as e:
                    _logger.info(e)
        
    
    def action_cancel(self):
        return