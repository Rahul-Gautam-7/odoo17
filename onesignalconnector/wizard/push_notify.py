from odoo import api,fields,models
import logging
import requests

_logger=logging.getLogger(__name__)

class PushNotify(models.TransientModel):
    _name="push.notify"
    _description="Wizard to notify"
    
    connector_ids=fields.Many2one('signal.connect',string="Onesignal AccountName")
    template_id=fields.Many2one('onesignal.template',string='Template')
  
    template=fields.Boolean(string="Using Template")
    action_btn=fields.Boolean(string="Action Button")
    
    heading=fields.Char(string="Heading")
    content=fields.Text(string="Content")
    cover_url=fields.Char(string="Cover URL")
    redirect_url=fields.Char(string="Redirect URL")
    abc=fields.Char(string="Channel",compute="_compute_abc",default="push")
    name=fields.Char(string="Channel",compute="_onchange_connect",default='push')
    
    template_domain = fields.Binary(compute="_compute_template_domain")
    action_btn_ids=fields.One2many('push.notify.button','notify_id',string="Action Button")
    subscription_id=fields.Many2many('user.fetch',string="Subscription_id")
    subscription_domain = fields.Binary(compute="_compute_subscription_domain")
     
     
    send_to=fields.Selection([
        ('all',"All"),
        ('subscription_id','Subscription_ID')
    ],string="Send To")
    notification_type=fields.Selection([
        ('push','Push Notification'),
        ('email','Email Notification'),
        ('sms','SMS Notification')
    ],string="Notification Type")
    
    email_subject = fields.Char(string="Email Subject")
    email_body = fields.Text(string="Email Body")
    recipient_email = fields.Char(string="Recipient Email")
    
    @api.depends('connector_ids')
    def _onchange_connect(self):
        self.name=self.connector_ids
        _logger.info(f"....................{self.name}")
       
    
   
    @api.depends('connector_ids', 'notification_type')
    def _compute_abc(self):
        for record in self:
            if record.notification_type == 'push' :
                record.abc = 'push'
            elif record.notification_type == 'email':
                record.abc = 'email'
            elif record.notification_type == 'sms':
                record.abc = 'sms'
            else:
                record.abc='push'
      
        
    @api.depends('notification_type','connector_ids')
    def _compute_template_domain(self):
        for rec in self:
            if rec.connector_ids and rec.notification_type:
                domain = [('connector_ids', '=', rec.connector_ids.ids),('channel', '=', rec.notification_type)]
            else:
                domain = [('id', '=', False)]
            rec.template_domain = domain 
                     
    
    @api.depends('connector_ids')
    def _compute_subscription_domain(self):
        for rec in self:
            if rec.connector_ids : 
                domain = [('connector_ids','in',rec.connector_ids.ids)]
                _logger.info(f"Subscription domain: {domain}")
            else:
                domain = [('id','=',False)]
            rec.subscription_domain = domain
            _logger.info(f"Computed domain: {domain}")  
        
        
        
        
        
    def action_send_notify(self):
      for record in self:
        app_id = record.connector_ids.app_id
        api_key = record.connector_ids.api_key
        
        if record.notification_type == 'push':
            if app_id:
                url = "https://onesignal.com/api/v1/notifications"
                
                player_ids = []
                for rec in self: 
                    if  rec.subscription_id:
                        rec.ensure_one() 
                        player_id = rec.subscription_id.player_id
                        player_ids.append(player_id)
                    else:
                        _logger.warning(f"No subscription found for record {rec.id}")

                payload = {
                    "app_id": app_id,
                    "include_player_ids": player_ids,
                    "template_id":record.template_id.temps_id,
                }

                if isinstance(record.content, str) and record.content.strip():
                    payload["contents"] = {"en": record.content}
                if isinstance(record.heading, str) and record.heading.strip():
                    payload["headings"] = {"en": record.heading}


                if record.send_to == 'all':
                    payload["included_segments"] = ["All"]
                elif record.send_to == 'subscription_id' and player_ids:
                    payload["include_player_ids"] = player_ids
                else:
                    _logger.info("Failed to send notification - No valid target.")
                    continue  

                if record.action_btn and record.action_btn_ids:
                    buttons = []
                    for button in record.action_btn_ids:
                        buttons.append({
                            "id": button.btn_id,
                            "text": button.btn_text,
                            "url": button.btn_url,
                        })
                    payload["buttons"] = buttons
                _logger.info(f"Payload being sent: {payload}")

                headers = {
                    'Authorization': f"Basic {api_key}",
                    'Content-Type': 'application/json',
                }
                try:  
                    response = requests.post(url, json=payload, headers=headers)
                    _logger.info(response.text)
                    if response.status_code == 200:
                        _logger.info(f"Notification Sent Success: {response.text}")
                    else:
                        _logger.error(f"Failed to send notification. Status code: {response.status_code}, Response: {response.text}")
                except Exception as e:
                    _logger.error(f"Error sending notification: {str(e)}")
        
    
    def action_cancel(self):
        return
 
    def _get_subscription_player_ids(self):
        player_ids = []

        if self.send_to == 'subscription_id':
            if self.subscription_id:  
               
                player_id = self.subscription_id.player_id
                if player_id:
                    player_ids.append(player_id)
                else:
                    _logger.warning(f"No player_id found for user: {self.subscription_id}")
            else:
                _logger.warning("No subscription_id selected.")
    
        return player_ids
    

class PushNotifyButton(models.TransientModel):
    _name="push.notify.button"
    _description="Push Notification Button "
    
    notify_id = fields.Many2one('push.notify',string="Push Notificaton")
    btn_id=fields.Char(string="Button Id")
    btn_text=fields.Char(string="Button Text")
    btn_url=fields.Char(string="Button URL")
