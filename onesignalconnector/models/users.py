from odoo import api,fields,models
import requests
import logging
from datetime import datetime

_logger=logging.getLogger(__name__)


DEVICE_TYPE_MAPPING = {
    0: 'ios',
    1: 'android',
    2: 'windows',
    5: 'chrome',
    6: 'safari',
    8: 'firefox',
    }


class User(models.Model):
    _name="user.fetch"
    _description="Fetching users"
    _rec_name="player_id"
    
    connector_ids=fields.Many2one('signal.connect',string="Name",ondelete='cascade')

    player_id=fields.Char(string="Player Id")
    app_id=fields.Char(related='connector_ids.app_id',store=True)
    api_key=fields.Char(related="connector_ids.api_key",store=True)
    

    identifier = fields.Char(string="Identifier")
    session_count = fields.Integer(string="Session Count")
    language = fields.Char(string="Language")
    timezone = fields.Integer(string="Time Zone")
    game_version = fields.Char(string="Game Version")
    device_os = fields.Char(string="Device OS")
    device_type = fields.Char(string="Device Type")
    types = fields.Char(string="Device Type")
    device_model = fields.Char(string="Device Model")
    ad_id = fields.Char(string="Ad ID")
    last_active = fields.Datetime(string="Last Active")
    playtime = fields.Float(string="Playtime")
    amount_spent = fields.Float(string="Amount Spent")
    created_at = fields.Datetime(string="Created At")
    invalid_identifier = fields.Boolean(string="Invalid Identifier")
    sdk = fields.Char(string="SDK Version")
    test_type = fields.Char(string="Test Type")
    ip = fields.Char(string="IP Address")
    tags = fields.Text(string="Tags")
    external_id=fields.Char(string="External ID")
    
    # signup_method = fields.Selection([
    #     ('webpush', 'WebPush'),
    #     ('email', 'Email'),
    #     ('sms', 'SMS')
    # ], string="Signup Method", required=True)
    
    # email = fields.Char("Email Address")
    # phone_number = fields.Char("Phone Number")
    # webpush_id = fields.Char("WebPush Identifier")
    
    
    
   
    
    
    
    
    @api.model
    def check_users(self,app_id):
        signal_records = self.env['signal.connect'].search([('id','=',app_id)])  
        _logger.info(f"Found {len(signal_records)} signal.connect records")
        for record in signal_records:   
            app_id = record.app_id
            api_key = record.api_key
            _logger.info(app_id)
            _logger.info(api_key)
            if app_id:
                url=f"https://onesignal.com/api/v1/players?app_id={app_id}"
                headers={
                "Authorization":f"Basic {api_key}",
                "Content-Type":"application/json",
                }
                try:
                    response = requests.get(url,headers=headers)
                    if response.status_code == 200 :
                        _logger.info("Users Fetch Success")
                        data=response.json()
                        for player in data.get('players', []):
                            player_id = player.get('id')

                            existing_player = self.search([
                                ('connector_ids', '=', record.id),
                                ('player_id', '=', player_id)
                            ], limit=1)
                        
                            if not existing_player:
                                self.create({
                                    'connector_ids': record.id,
                                    'player_id': player_id,
                                    'identifier': player.get('identifier'),
                                    'session_count': player.get('session_count', 0),
                                    'language': player.get('language'),
                                    'timezone': player.get('timezone', 0),
                                    'game_version': player.get('game_version', ''),
                                    'device_os': player.get('device_os', ''),
                                    'device_type': DEVICE_TYPE_MAPPING.get(player.get('device_type')),
                                    'types': player.get('type'),
                                    'device_model': player.get('device_model', ''),
                                    'ad_id': player.get('ad_id', ''),
                                    'last_active': datetime.utcfromtimestamp(player.get('last_active')),
                                    'playtime': player.get('playtime', 0.0),
                                    'amount_spent': player.get('amount_spent', 0.0),
                                    'created_at': datetime.utcfromtimestamp(player.get('created_at')),
                                    'invalid_identifier': player.get('invalid_identifier', False),
                                    'sdk': player.get('sdk', ''),
                                    'test_type': player.get('test_type', None),
                                    'ip': player.get('ip', ''),
                                    'tags': str(player.get('tags', {})),
                                    'external_id':player.get('external_id', ''),  
                                })
                            else:
                                _logger.info(f"Player {player_id} already exists.")
                    else:
                        _logger.info("User Fetch Failure")
                except requests.exceptions.RequestException as e:
                    _logger.info("Error in sending notifiy",str(e))
    
    
    
    
    # def create_user_in_onesignal(self):
    #     for record in self:
    #         app_id = record.connector_ids.app_id
    #         api_key = record.connector_ids.api_key

    #         if not app_id or not api_key:
    #             _logger.error("Missing OneSignal App ID or API Key.")
    #             return False

    #         url = f"https://api.onesignal.com/apps/{app_id}/users"

    #         # Build the payload to create a user based on the notification type
    #         payload = {
    #             "app_id": app_id,
    #             "identifier": record.user_email,  # The unique identifier (email in this case)
    #             "language": "en",  # You can set a language if required
    #             "tags": {
    #                 "email": record.user_email  # You can customize tags as required
    #             }
    #         }

    #         if record.notification_type == 'push':
    #             # For Push Notifications
    #             payload["device_type"] = 1 if record.device_type == 'android' else 0  # 1 for Android, 0 for iOS
    #             if record.player_id:
    #                 payload["player_id"] = record.player_id  # Set player ID for push
    #             _logger.info(f"Creating push user with Player ID: {record.player_id}")

    #         elif record.notification_type == 'email':
    #             # For Email Notifications
    #             payload["email"] = record.user_email  # Register the email for email notifications
    #             _logger.info(f"Creating email user with Email: {record.user_email}")

    #         elif record.notification_type == 'sms':
    #             # For SMS Notifications
    #             payload["sms"] = record.user_email  # You can register phone number or email for SMS notifications
    #             _logger.info(f"Creating SMS user with Phone Number/Email: {record.user_email}")

    #         headers = {
    #             "Authorization": f"Basic {api_key}",
    #             "Content-Type": "application/json",
    #         }

    #         try:
    #             response = requests.post(url, json=payload, headers=headers)
    #             if response.status_code == 200:
    #                 _logger.info(f"Successfully created user in OneSignal: {response.json()}")
    #                 return True
    #             else:
    #                 _logger.error(f"Failed to create user in OneSignal. Status Code: {response.status_code}, Response: {response.text}")
    #                 return False
    #         except Exception as e:
    #             _logger.error(f"Error creating user in OneSignal: {str(e)}")
    #             return False
    
    
    def create_user_in_onesignal(self):
        for rec in self:
            app_id=rec.app_id
            api_key=rec.api_key
            
            _logger.info(f"............................................................{app_id}")
            _logger.info(f"............................................................{api_key}")
            
            url=f"https://api.onesignal.com/apps/{app_id}/users"
            
            payload = {
                "device_type":int(self.device_type),
                 "properties": {
                        "ip":self.ip,
                    },
                "identity": { "external_id": self.external_id },
                "tags": {  
                "subscription_status": "subscribed",  
                }
            }
            _logger.info(f"payload value........................{payload}")
            
            headers = {
                    "Authorization": f"Basic {api_key}",
                    "Content-Type": "application/json",
                }
            
            try:
                response= requests.post(url,json=payload,headers=headers)
                
                if response.status_code == 200:
        
                    _logger.info("success=================================================SUCCESS===========================")

                else:
                    _logger.error(f"User creation failed: {response.status_code}, {response.text}")
            except requests.exceptions.RequestException as e:
                    _logger.error(f"Error creating user in OneSignal: {str(e)}")
       
    
    
    
    
  