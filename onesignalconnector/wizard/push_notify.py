from odoo import api,fields,models
import logging
import requests

_logger=logging.getLogger(__name__)

class PushNotify(models.TransientModel):
    _name="push.notify"
    _description="Wizard to notify"
    
    connector_ids=fields.Many2one('signal.connect',string="Onesignal AccountName")
    template_id=fields.Many2one('onesignal.template',string='Template')
    segment_id=fields.Many2many('onesignal.segment',string="Segments")
  
    template=fields.Boolean(string="Using Template")
    action_btn=fields.Boolean(string="Action Button")
    heading=fields.Char(string="Heading")
    content=fields.Text(string="Content")
    chrome_web_image=fields.Char(string="Cover URL")
    redirect_url=fields.Char(string="Redirect URL")
    abc=fields.Char(string="Channel",compute="_compute_abc",default="push")
    name=fields.Char(string="Channel",compute="_onchange_connect",default='push')
    template_domain = fields.Binary(compute="_compute_template_domain")
    action_btn_ids=fields.One2many('push.notify.button','notify_id',string="Action Button")
    subscription_id=fields.Many2many('user.fetch',string="Subscription_id")
    subscription_domain = fields.Binary(compute="_compute_subscription_domain")
    segment_domain=fields.Binary(compute="_compute_segments_domain")
    send_to=fields.Selection([
        ('all',"All"),
        ('segments',"Segments"),
        ('subscription_id','Subscription_ID')
    ],string="Send To",default="all")
    notification_type=fields.Selection([
        ('push','Push Notification'),
        ('email','Email Notification'),
        ('sms','SMS Notification')
    ],string="Notification Type",default="push")
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
    def _compute_segments_domain(self):
        for rec in self:
            if rec.connector_ids :
                domain=[('connector_ids','=',rec.connector_ids.ids)]
            else :
                domain = [('id','=',False)]
            rec.segment_domain = domain
    
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
        
        if record.notification_type:
            if app_id:
                if record.notification_type == 'push':
                    url = "https://onesignal.com/api/v1/notifications?c=push"
                
                    payload = {
                        "app_id": app_id,
                        "template_id": record.template_id.temps_id,
                        "language":"en",
                        "chrome_web_image":record.chrome_web_image,
                    }
                elif record.notification_type == 'email':
                    url = "https://onesignal.com/api/v1/notifications?c=email"
                    payload = {
                                "app_id": app_id,
                                "email_subject": "This is your email subject.",
                                "email_body": "<html>Your Email as HTML.</html>",
                                "email_to":["gautamrahul1234567890@gmail.com"]
                        }   
                 
                if record.send_to == 'all':
                    payload["included_segments"] = ["All"]
                
                elif record.segment_id and record.segment_id.mapped("name"):
                    segment_value = record.segment_id.mapped("name")
                    payload["included_segments"] = segment_value
                    segment_names = ", ".join(segment_value)  
                    _logger.info(f"Sending to selected segments: {segment_names}")
                        
                elif record.send_to == 'subscription_id':
                    player_ids = []
                    for rec in self:
                        if rec.subscription_id:
                            rec.ensure_one()
                            for sub in rec.subscription_id:                        
                                player_id = sub.player_id
                                player_ids.append(player_id)
                                _logger.info(f"Found player_id for record {rec.id}: {player_id}")
                        else:
                           if not rec.subscription_id:
                                _logger.warning(f"Subscription ID is missing for record {rec.id}. Skipping this record.")
                                continue

                    if player_ids:
                        payload["include_player_ids"] = player_ids
                        _logger.info(f"Sending to player IDs: {player_ids}")
                    else:
                        _logger.warning("Failed to send notification - No valid subscription IDs.")
                        continue
                    
                if isinstance(record.content, str) and record.content.strip():
                    payload["contents"] = {"en": record.content}  
                if isinstance(record.heading, str) and record.heading.strip():
                    payload["headings"] = {"en": record.heading }
              
                if record.action_btn and record.action_btn_ids:
                    buttons = []
                    for button in record.action_btn_ids:
                        buttons.append({
                            "id": button.btn_id,
                            "text": button.btn_text,
                            "url": button.btn_url,
                        })
                    payload["web_buttons"] = buttons

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
    
    def cron_notify(self):
       
        connectors = self.env['signal.connect'].search([])  
        for connector in connectors:
            app_id = connector.app_id
            api_key = connector.api_key

            if not app_id or not api_key:
                _logger.error(f"App ID or API Key is missing for app: {connector.name}")
                continue

            url = "https://onesignal.com/api/v1/notifications"

            payload = {
                "app_id": app_id,
                "included_segments": ["All"],  
                "contents": {"en": "This is a notification from the cron job."},
                "headings": {"en": "Cron Job Notification"},
                "chrome_web_image":"https://cdn3.pixelcut.app/7/20/uncrop_hero_bdf08a8ca6.jpg",
            }

            headers = {
                'Authorization': f"Basic {api_key}",
                'Content-Type': 'application/json',
            }
            try:
                response = requests.post(url, json=payload, headers=headers)
                _logger.info(f"Response from OneSignal for app_id {app_id}: {response.text}")
                if response.status_code == 200:
                    _logger.info(f"Notification Sent Successfully for app_id: {app_id}")
                else:
                    _logger.error(f"Failed to send notification for app_id {app_id}. Status code: {response.status_code}, Response: {response.text}")
            except Exception as e:
                _logger.error(f"Error sending notification for app_id {app_id}: {str(e)}")
 
    
class PushNotifyButton(models.TransientModel):
    _name="push.notify.button"
    _description="Push Notification Button "
    
    notify_id = fields.Many2one('push.notify',string="Push Notificaton")
    btn_id=fields.Char(string="Button Id")
    btn_text=fields.Char(string="Button Text")
    btn_url=fields.Char(string="Button URL")
