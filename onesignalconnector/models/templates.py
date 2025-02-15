from odoo import api,fields,models
import requests
import logging

_logger = logging.getLogger(__name__)

class Templates(models.Model):
    _name="onesignal.template"
    _description="One signal segments"
    
    name=fields.Char(string="Template Name")
    temps_id=fields.Char(string="Template Id")
    connector_ids=fields.Many2one('signal.connect',string="connector ID")
    app_id=fields.Char(related="connector_ids.app_id",store=True)
    api_key=fields.Char(related="connector_ids.api_key",store=True)
    channel=fields.Selection([
        ('push',"Push"),
        ('email',"Email"),
        ('sms','SMS')
    ],string="Channel")
    
    headings=fields.Char(string="Headings")
    subtitle=fields.Char(string="Subtitle")
    contents=fields.Text(string="Contents")
    global_image=fields.Text(string="GlobalImage")
    url_link=fields.Char(string="url_link")
    
    is_Email = fields.Boolean(string="Email Available")
    email_body = fields.Text(string="Email Body")
    email_subject = fields.Char(string="Email Subject")
    email_preheader = fields.Char(string="Email Preheader")
    email_reply_to_address = fields.Char(string="Reply-to Email Address")
    disable_email_click_tracking = fields.Boolean(string="Disable Email Click Tracking")

    is_SMS = fields.Boolean(string="SMS Available")
    sms_from = fields.Char(string="SMS From")
    sms_media_urls = fields.Text(string="SMS Media URLs")
    
    is_android = fields.Boolean(string="Android")
    is_ios = fields.Boolean(string="iOS")
    is_macosx = fields.Boolean(string="MacOSX")
    is_adm = fields.Boolean(string="ADM")
    is_alexa = fields.Boolean(string="Alexa",readonly=True)
    is_wp = fields.Boolean(string="Windows Phone")
    is_wp_wns = fields.Boolean(string="Windows Phone WNS")
    is_chrome = fields.Boolean(string="Chrome")
    is_chrome_web = fields.Boolean(string="Chrome Web")
    is_safari = fields.Boolean(string="Safari")
    is_firefox = fields.Boolean(string="Firefox")
    is_edge = fields.Boolean(string="Edge")
    
    
    @api.model
    def create(self, values):
        sync_user = self.env.context.get('sync_template', False)
        if not sync_user:
            user = super(Templates, self).create(values)
            user.create_template_in_onesignal()
            return user
        else:
            return super(Templates, self).create(values)
    
    
    @api.model
    def check_templates(self,app_id):
        signal_rec = self.env['signal.connect'].search([('id','=',app_id)])
        for record in signal_rec:
            app_id=record.app_id
            api_key=record.api_key
            if app_id:
                url=f"https://api.onesignal.com/templates?app_id={app_id}"
                
                headers={
                    'Authorization':f"Basic {api_key}",
                    'Content-Type':'application/json',
                }
                try:
                    response = requests.get(url,headers=headers)
                    _logger.info(response)
                    if response.status_code == 200:
                        data = response.json()
                        _logger.info(data)
                        
                        templates_list = data.get('templates', [])
    
                        for templatess in data.get('templates',[]):
                            _logger.info(f"Fetched template: {templatess}")
                            temps_id=templatess.get('id')
                            
                            
                            detail_url = f"https://api.onesignal.com/templates/{temps_id}?app_id={app_id}"
                            detail_response = requests.get(detail_url, headers=headers)
                            
                            if detail_response.status_code == 200:
                                detail_data = detail_response.json()
                                _logger.info(f"Detailed data for template {temps_id}: {detail_data}")
                            
                            
                                content_data = detail_data.get('content', {})
                   
                                existing_template = self.env['onesignal.template'].search([
                                ('connector_ids', '=', record.id),
                                ('temps_id', '=', temps_id),
                                ], limit=1)

                                if not existing_template:
                                    self.with_context(sync_template=True).create({
                                        'connector_ids': record.id,
                                        'temps_id': temps_id,
                                        'name': templatess.get('name'),
                                        'channel': templatess.get('channel'),
                                        'headings': content_data.get('headings', {}).get('en', ''),
                                        'contents':content_data.get('contents', {}).get('en', ''),
                                        'url_link':content_data.get('url', ''),
                                        'subtitle':content_data.get('subtitle', ''),
                                        'global_image':content_data.get('global_image', ''),
                                        'is_android': content_data.get('isAndroid', False),
                                        'is_ios': content_data.get('isIos', False),
                                        'is_macosx': content_data.get('isMacOSX', False),
                                        'is_adm': content_data.get('isAdm', False),
                                        'is_alexa': content_data.get('isAlexa', False),
                                        'is_wp': content_data.get('isWP', False),
                                        'is_wp_wns': content_data.get('isWP_WNS', False),
                                        'is_chrome': content_data.get('isChrome', False),
                                        'is_chrome_web': content_data.get('isChromeWeb', False),
                                        'is_safari': content_data.get('isSafari', False),
                                        'is_firefox': content_data.get('isFirefox', False),
                                        'is_edge': content_data.get('isEdge', False),
                                        'is_Email': content_data.get('is_Email',False),
                                        'email_body': content_data.get('email_body'),
                                        'email_subject': content_data.get('email_subject'),
                                        'email_preheader': content_data.get('email_preheader'),
                                        'email_reply_to_address': content_data.get('email_reply_to_address'),
                                        'disable_email_click_tracking': content_data.get('disable_email_click_tracking'),
                                        'is_SMS': content_data.get('is_SMS'),
                                        'sms_from': content_data.get('sms_from'),
                                        'sms_media_urls': content_data.get('sms_media_urls')
                                    })
                                else:
                                    _logger.info("Template already exists, skipping creation")
                            else:
                                _logger.error(f"Failed to fetch details for template {temps_id}")
                    else:
                        _logger.error(f"Failed to fetch templates. Status code: {response.status_code}")
            
                except requests.exceptions.RequestException as e:
                    _logger.error(f"Error while fetching templates: {str(e)}")
                            
                            
 
    def create_template_in_onesignal(self):
        for rec in self:
            app_id=rec.app_id
            api_key=rec.api_key
            
            url="https://api.onesignal.com/templates"
            
            payload = {
                    "app_id":app_id,
                    "name":rec.name,
                    "channel":rec.channel,
                    "headings": {"en":rec.headings},
                    "contents": {"en":rec.contents}
            }
            _logger.info(f"--------------------------------------------{payload}")
            if rec.channel == 'sms':
                payload.update({
                    "sms_from": rec.sms_from,
                    "sms_media_urls": [rec.sms_media_urls]
                })
                _logger.info(f"SMS template, added fields: {payload}")
        
           
            elif rec.channel == 'email':
                payload.update({
                    "email_body": rec.email_body,
                    "email_subject": rec.email_subject,
                    "email_preheader": rec.email_preheader,
                    "email_reply_to_address": rec.email_reply_to_address,
                    "disable_email_click_tracking": rec.disable_email_click_tracking
                })
                _logger.info(f"Email template, added fields: {payload}")
            
            else :
                payload.update({
                                'isAndroid': rec.is_android,
                                'isIos': rec.is_ios,
                                'isMacOSX': rec.is_macosx,
                                'isAdm': rec.is_adm,
                                'isWP': rec.is_wp,
                                'isWP_WNS': rec.is_wp_wns,
                                'isChrome': rec.is_chrome,
                                'isChromeWeb': rec.is_chrome_web,
                                'isSafari': rec.is_safari,
                                'isFirefox': rec.is_firefox,
                                'isEdge': rec.is_edge,
                })
                _logger.info(f"Push template----------------{payload}")
             
            headers = {
                    "Authorization": f"Basic {api_key}",
                    "Content-Type": "application/json",
                }
            
            try:
                response= requests.post(url,json=payload,headers=headers)
                
                if response.status_code == 200:
                    self.connector_ids.action_sync_templates()
                    _logger.info("success=================================================SUCCESS===========================")
                else:
                    _logger.error(f"User creation failed: {response.status_code}, {response.text}")
            except requests.exceptions.RequestException as e:
                    _logger.error(f"Error creating user in OneSignal: {str(e)}")
                    
                    
    def update_template_in_onesignal(self):
            app_id=self.app_id
            api_key=self.api_key
            
            url=f"https://api.onesignal.com/templates/{self.temps_id}?app_id={app_id}"
            
            payload = {
                    "app_id":app_id,
                    "name":self.name,
                    "channel":self.channel,
                    "is_chrome":self.is_chrome,
                    "is_chrome_web":self.is_chrome_web,
                    "headings": {"en":self.headings},
                    "contents": {"en":self.contents}
            }
    
            _logger.info(f"payload value........................{payload}")
            
            headers = {
                    "Authorization": f"Basic {api_key}",
                    "Content-Type": "application/json",
                }
            try:
                response= requests.patch(url,json=payload,headers=headers)
                
                if response.status_code == 200:
                    _logger.info("success=================================================SUCCESS===========================")
                else:
                    _logger.error(f"User creation failed: {response.status_code}, {response.text}")
            except requests.exceptions.RequestException as e:
                    _logger.error(f"Error creating user in OneSignal: {str(e)}")
                    
    
    def delete_templates(self):
        for rec in self:
            app_id=rec.app_id
            api_key=rec.api_key
            _logger.info(f"player app_id....................................{app_id}")
            _logger.info(f"player api_key....................................{api_key}")
            
            url = f"https://api.onesignal.com/templates/{rec.temps_id}?app_id={app_id}"
            headers = {
                "accept": "application/json",
                "Authorization": f"Basic {api_key}"
            }
            response = requests.delete(url, headers=headers)
            self.unlink()
            _logger.info(f"user deleted ..........................................{response}")
        return