from odoo import api,fields,models
import requests
import logging
from datetime import datetime
from odoo.exceptions import ValidationError
from datetime import datetime

_logger=logging.getLogger(__name__)

DEVICE_TYPE_MAPPING = {
    0: 'iOS',
    1: 'Android',
    2: 'Amazon',
    3: 'Windows Phone (MPNS)',
    4: 'Chrome Apps / Extensions',
    5: 'Chrome Web Push',
    6: 'Windows (WNS)',
    7: 'Safari',
    8: 'Firefox',
    9: 'MacOS',
    10: 'Alexa',
    11: 'Email',
    13: 'Huawei App Gallery Builds',
    14: 'SMS',
    17: 'Safari'
}

TYPE_MAPPING = {
    'email': 'Email',
    'sms': 'SMS',
    'iOSPush': 'iOS Push',
    'AndroidPush': 'Android Push',
    'HuaweiPush': 'Huawei Push',
    'FireOSPush': 'Fire OS Push',
    'WindowsPush': 'Windows Push',
    'macOSPush': 'macOS Push',
    'ChromeExtensionPush': 'Chrome Extension Push',
    'ChromePush': 'Chrome Push',
    'FirefoxPush': 'Firefox Push',
    'SafariPush': 'Safari Push',
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
    types = fields.Char(string="Type")
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
    external_id=fields.Char(string="External ID",store=True)
    token=fields.Char(string="Token")
    current_timestamp = datetime.utcnow().strftime('%Y-%m-%d%H:%M:%S')
 

    
    channel = fields.Selection([
        ('webpush', 'Web Push'),
        ('email', 'Email'),
        ('sms', 'SMS'),
    ], string="Notification Type", required=True, default='webpush')
    

    @api.model
    def create(self, values):
        sync_user = self.env.context.get('sync_user', False)
        if not sync_user:
            user = super(User, self).create(values)
            user.create_user_in_onesignal()
            return user
        else:
            return super(User, self).create(values)
        
    
    @api.model
    def check_users(self,app_id):
            signal_records = self.env['signal.connect'].search([('id','=',app_id)])  
            if app_id:
                url=f"https://onesignal.com/api/v1/players?app_id={signal_records.app_id}"
                headers={
                "Authorization":f"Basic {signal_records.api_key}",
                "Content-Type":"application/json",
                }
                try:
                    response = requests.get(url,headers=headers)
                    if response.status_code == 200 :
                        data=response.json()
                        
                        # onesignal_players = data.get('players', [])
                        # onesignal_player_ids = {player.get('id') for player in onesignal_players}
                        # odoo_players = self.search([('connector_ids', '=', signal_records.id)])
                        # odoo_player_ids = {player.player_id for player in odoo_players}
                        # players_to_remove = odoo_players.filtered(lambda p: p.player_id not in onesignal_player_ids)       
                        # for player in players_to_remove:
                        #     _logger.info(f"Removing player {player.player_id} from Odoo as they no longer exist in OneSignal.")
                        #     player.unlink()
                            

                        for player in data.get('players', []):
                            player_id = player.get('id')
                            existing_player = self.search([
                                ('player_id', '=', player_id),
                            ], limit=1)
                            
                            player_id = player.get('id', '')
                            existing_user=self.search([('player_id', '=', player_id)], limit=1)
                            values={
                                    'connector_ids': signal_records.id,
                                    'player_id': player_id,
                                    'identifier': player.get('identifier'),
                                    'session_count': player.get('session_count', 0),
                                    'language': player.get('language'),
                                    'timezone': player.get('timezone', 0),
                                    'game_version': player.get('game_version', ''),
                                    'device_os': player.get('device_os', ''),
                                    'device_type': DEVICE_TYPE_MAPPING.get(player.get('device_type')),
                                    'types': TYPE_MAPPING.get(player.get('type'), 'Unknown'),
                                    'device_model': player.get('device_model', ''),
                                    'ad_id': player.get('ad_id', ''),
                                    'last_active': datetime.utcfromtimestamp(player.get('last_active')),
                                    'playtime': player.get('playtime', 0.0),
                                    'amount_spent': player.get('amount_spent', 0.0),
                                    'created_at': datetime.utcfromtimestamp(player.get('created_at')),
                                    'invalid_identifier': player.get('invalid_identifier', False),
                                    'sdk': player.get('sdk', ''),
                                    'token':player.get('token', ''),
                                    'test_type': player.get('test_type', None),
                                    'ip': player.get('ip', ''),
                                    'tags': str(player.get('tags', {})),
                                    'external_id':player.get('external_user_id', ''),
                            }
                            if existing_user:
                                existing_user.write(values)
                            else:
                                self.with_context(sync_user=True).create(values)          
                except requests.exceptions.RequestException as e:
                    _logger.info("Error in sending notifiy",str(e))
                
    
    def create_user_in_onesignal(self):
            self.ensure_one()
            if self.channel == 'webpush':
                token=self.token
                if not self.token:
                    raise ValidationError("Token is required when the notification type is WebPush.")
                tp = "ChromePush"
                payload = {
                    "subscriptions":[   {"type": tp,"token":self.token,"enabled":True}    ],
                    "tags": {  "subscription_status": "subscribed",  },
                    "identity":{"external_id" : f"{self.token}_{self.current_timestamp}" },
                    }
            elif self.channel == 'email':
                if not self.token:
                    raise ValidationError("Token is required when the notification type is Email.")
                if '@' not in self.token:
                    raise ValidationError("A valid email address must be provided when the notification type is Email.")    
                tp = "Email"
                token = self.token
                payload = {
                    "subscriptions":[   {"type": tp,"token":token,"enabled":True}  ],
                    "tags": {  "subscription_status": "subscribed",  },
                    "identity":{"external_id" : f"{self.token}_{self.current_timestamp}" },
                    }
            elif self.channel == 'sms':
                if not self.token:
                    raise ValidationError("Phone number is required when the notification type is SMS.")
                if len(self.token) != 10:
                    raise ValidationError("Phone number must be 10 digits when the notification type is SMS.")
                tp = "SMS"
                token= f"+{self.token}" if not self.token.startswith("+") else self.token
                payload = {
                    "subscriptions":[   {"type": tp,"token":token,"enabled":True}  ],
                    "tags": {  "subscription_status": "subscribed",  },
                    "identity":{"external_id" : f"{self.token}_{self.current_timestamp}" },
                    } 
            else:
                _logger.error("Invalid notification type specified")
                return
            
            url=f"https://api.onesignal.com/apps/{self.app_id}/users"
            
            headers = {
                    "Authorization": f"Basic {self.api_key}",
                    "Content-Type": "application/json",
                }
            response= requests.post(url,json=payload,headers=headers)        
            if response.status_code == 201:
                self.connector_ids.action_sync_user()          
            else:
                 _logger.error(f"User creation failed: {response.status_code}, {response.text}")
            
                    
    def update_user_in_onesignal(self):            
            url=f"https://api.onesignal.com/apps/{self.app_id}/users/by/external_id/{self.external_id}"
            
            if self.channel == 'webpush':
                tp = "ChromePush"
                payload = {
                    "subscriptions":[   {"type": tp,"enabled":True}    ],
                    "tags": {  "subscription_status": "subscribed",  }
                    }
               
            elif self.channel == 'email':
                tp = "Email"
                token = self.token
                payload = {
                    "properties": { "ip":self.ip, },
                    "subscriptions":[   {"type": tp,"token":token,"enabled":True}  ],
                    "tags": {  "subscription_status": "subscribed",  }
                    }
    
            elif self.channel == 'sms':
                tp = "SMS"
                token= f"+{self.token}" if not self.token.startswith("+") else self.token
                payload = {
                    "subscriptions":[   {"type": tp,"token":token,"enabled":True}  ],
                    "tags": {  "subscription_status": "subscribed",  }
                    } 
            else:
                return
          
            if self.external_id:
                payload["identity"] = {"external_id": self.external_id}
            headers = {
                    "Authorization": f"Basic {self.api_key}",
                    "Content-Type": "application/json",
                }
            response= requests.patch(url,json=payload,headers=headers) 
            if response.status_code == 200:
                _logger.info("success=================================================SUCCESS===========================")
               
    
    def delete_user(self):
            url = f"https://onesignal.com/api/v1/players/{self.player_id}?app_id={self.app_id}"

            headers = {
                "accept": "application/json",
                "Authorization": f"Basic {self.api_key}"
            }
            response = requests.delete(url, headers=headers)
            if response.status_code == 200:
                self.unlink()
                _logger.info("success=================================================SUCCESS===========================")
            else:
                    _logger.error(f"User creation failed: {response.status_code}, {response.text}")
                    return