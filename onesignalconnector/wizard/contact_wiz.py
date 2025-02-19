from odoo import api,fields,models
import requests
import logging
from datetime import datetime
from odoo.exceptions import ValidationError
import re



_logger=logging.getLogger(__name__)


class ContactWiz(models.TransientModel):
    _name = 'contact.wizard'
    _description = 'Subscribe Contact to OneSignal'

    connector_ids=fields.Many2one('signal.connect',string="Onesignal AccountName")

    current_timestamp = datetime.utcnow().strftime('%Y-%m-%d%H:%M:%S')

    
    
    def _default_contact(self):
        return self.env.context.get('active_id')

    def _default_email(self):
        contact = self.env['res.partner'].browse(self.env.context.get('active_id'))
        return contact.email

    def _default_phone(self):
        contact = self.env['res.partner'].browse(self.env.context.get('active_id'))
        return contact.phone
    
    
    def _default_tags(self):
            contact = self.env['res.partner'].browse(self.env.context.get('active_id'))
            return ', '.join(contact.category_id.mapped('name'))
    
    
 
    contact_id = fields.Many2one('res.partner', string='Contact', default=_default_contact,readonly=True)
    notification_type=fields.Selection([
        ('email', 'Email'),
        ('sms', 'SMS')
        ],string="Notification Type")
    email = fields.Char(string='Email', default=_default_email)
    phone = fields.Char(string='Phone', default=_default_phone)
    tags=fields.Char(string="Tags", default=_default_tags)
    
   
   
    
    
    def subscribe_to_onesignal(self): 
        if self.email and self.notification_type == 'email':
            if self._is_already_subscribed(self.email):
                _logger.info("---------------------------------------------VALIDATION ERROR EMAIL-------------------")
                raise ValidationError("This email is already subscribed to OneSignal.")
            else:
                self._subscribe_to_onesignal(self.email)
                
        elif self.phone and self.notification_type == 'sms':
            if self._is_already_subscribed(self.phone):
                _logger.info("---------------------------------------------VALIDATION ERROR PHONE-------------------")
                raise ValidationError("This phone number is already subscribed to OneSignal.")
            else:
                pattern = r'^\d{10,15}$'
                if not re.match(pattern, self.phone):
                    raise ValidationError("Invalid phone number format. The phone number must consist of 10 to 15 digits.")
               
                self._subscribe_to_onesignal(self.phone)
        
        else:
            raise ValidationError("You Dont have Email and Phone number")
        
        
    def _is_already_subscribed(self, identifier):
        _logger.info(f"---------------------------------------------{identifier}")
        onesignal_app_id = self.connector_ids.app_id
        onesignal_rest_api_key = self.connector_ids.api_key
        onesignal_url = f"https://api.onesignal.com/apps/{onesignal_app_id}/users/by/external_id/+{identifier}"

        headers = {
            "Content-Type": "application/json",
            "Authorization": f"Basic {onesignal_rest_api_key}",
        }

        response = requests.get(onesignal_url, headers=headers)
        _logger.info(f"%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%{response.status_code}")
        if response.status_code == 200:
                return True 
        return False  

    def _subscribe_to_onesignal(self, identifier):
        _logger.info(f"----------------------------------------------------------------{identifier}")
       
        onesignal_app_id = self.connector_ids.app_id
        onesignal_rest_api_key = self.connector_ids.api_key
        url=f"https://api.onesignal.com/apps/{onesignal_app_id}/users"

        headers = {
            "Content-Type": "application/json",
            "Authorization": f"Basic {onesignal_rest_api_key}",
        }
        types=''
        if identifier == self.email:
            types='Email'
        else:
            identifier=f"+{identifier}" if not identifier.startswith("+") else self.identifier
            types='SMS'
            

        payload = { 
                    "subscriptions":[   {"type":types,"token":identifier,"enabled":True}  ],
                    "properties":{
                         "tags":{  
                             "subscription_status":self.tags  
                             },
                      
                    },
                    "identity":{"external_id" : f"{identifier}" },
                    } 

        response = requests.post(url, json=payload, headers=headers)
        _logger.info(f"-----------------------------------------------------{response.status_code}")
        if response.status_code == 200 or response.status_code == 201:
            _logger.info(f"--------------------------success=================================--===============")
            connector = self.env['signal.connect'].search([], limit=1) 
            connector.action_sync_user()
            return True
        else:
            return False
