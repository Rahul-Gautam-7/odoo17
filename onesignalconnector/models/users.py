from odoo import api,fields,models
import requests
import logging
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
    email = fields.Char("Email")
    phone_number = fields.Char("Phone Number")

 

    
    channel = fields.Selection([
        ('webpush', 'Web Push'),
        ('email', 'Email'),
        ('sms', 'SMS'),
    ], string="Notification Type", required=True, default='webpush')
    
    
    
    @api.model
    def create(self, vals):
        # Create the record
        new_record = super(User, self).create(vals)
        # If the player_id is missing, delete the record
        if not new_record.player_id:
            new_record.unlink()
            _logger.info("Record with no player_id has been deleted.")
        return new_record

    
    @api.model
    def check_users(self,app_id=None):
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
                            external_id=player.get('identity', {})
                            _logger.info(f"============================================================{external_id}")

                            existing_player = self.search([
                                ('connector_ids', '=', record.id),
                                ('player_id', '=', player_id),
                            ], limit=1)
                        
                            if existing_player:
                               
                            # Update existing player if changes exist
                                existing_player.write({
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
                                    'phone_number': player.get('phone_number', ''),
                                    'email': player.get('email', ''),
                                    'test_type': player.get('test_type', None),
                                    'ip': player.get('ip', ''),
                                    'tags': str(player.get('tags', {})),
                                    'external_id': player.get('external_user_id', ''),
                   
                                })
                                _logger.info(f"Player {player_id} updated.")
                            else : 
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
                                    'types': TYPE_MAPPING.get(player.get('type'), 'Unknown'),
                                    'device_model': player.get('device_model', ''),
                                    'ad_id': player.get('ad_id', ''),
                                    'last_active': datetime.utcfromtimestamp(player.get('last_active')),
                                    'playtime': player.get('playtime', 0.0),
                                    'amount_spent': player.get('amount_spent', 0.0),
                                    'created_at': datetime.utcfromtimestamp(player.get('created_at')),
                                    'invalid_identifier': player.get('invalid_identifier', False),
                                    'sdk': player.get('sdk', ''),
                                    'phone_number':player.get('phone_number', ''),
                                    'email':player.get('email', ''),
                                    'test_type': player.get('test_type', None),
                                    'ip': player.get('ip', ''),
                                    'tags': str(player.get('tags', {})),
                                    'external_id':player.get('external_user_id', ''),
                                })
                         
                    else:
                        _logger.info("User Fetch Failure")
                except requests.exceptions.RequestException as e:
                    _logger.info("Error in sending notifiy",str(e))
                
    
    
    
    
    
    def create_user_in_onesignal(self):
        for rec in self:
            rec.ensure_one()
            app_id=rec.app_id
            api_key=rec.api_key
            
            url=f"https://api.onesignal.com/apps/{app_id}/users"
            
        
            if rec.channel == 'webpush':
                tp = "ChromePush"
                payload = {
                    "properties": { "ip":self.ip  },
                    "subscriptions":[   {"type": tp,"enabled":True}    ],
                    "tags": {  "subscription_status": "subscribed",  },
                    }
               
            elif rec.channel == 'email':
                tp = "Email"
                token = rec.email
                payload = {
                    "properties": { "ip":self.ip, },
                    "subscriptions":[   {"type": tp,"token":token,"enabled":True}  ],
                    "tags": {  "subscription_status": "subscribed",  }
                    }
    
            elif rec.channel == 'sms':
                tp = "SMS"
                token= f"+{rec.phone_number}" if not rec.phone_number.startswith("+") else rec.phone_number
                payload = {
                    "properties": {"ip":self.ip},
                    "subscriptions":[   {"type": tp,"token":token,"enabled":True}  ],
                    "tags": {  "subscription_status": "subscribed",  }
                    } 
            else:
                _logger.error("Invalid notification type specified")
                return
            
            
            if rec.external_id:
                payload["external_user_id"] = rec.external_id,
    
                _logger.info(f"payload value........................{payload}")
            
            headers = {
                    "Authorization": f"Basic {api_key}",
                    "Content-Type": "application/json",
                }
            
        
            response= requests.post(url,json=payload,headers=headers)
            _logger.info(f"-------------------------------------------{response.status_code}")
                
            if response.status_code == 201:
                self.connector_ids.action_sync_user()
                _logger.info("success=================================================SUCCESS Creating Record===========================")
                    
            else:
                 _logger.error(f"User creation failed: {response.status_code}, {response.text}")
            
                    
                    
                    
                    
    def update_user_in_onesignal(self):
            app_id=self.app_id
            api_key=self.api_key
            external_id=self.external_id

            _logger.info(f"...............................................{external_id}")
            
            url=f"https://api.onesignal.com/apps/{app_id}/users/by/external_id/{external_id}"
            
        
            if self.channel == 'webpush':
                tp = "ChromePush"
                payload = {
                    "properties": { "ip":self.ip  },
                    "subscriptions":[   {"type": tp,"enabled":True}    ],
                    "tags": {  "subscription_status": "subscribed",  }
                    }
               
            elif self.channel == 'email':
                tp = "Email"
                token = self.email
                payload = {
                    "properties": { "ip":self.ip, },
                    "subscriptions":[   {"type": tp,"token":token,"enabled":True}  ],
                    "tags": {  "subscription_status": "subscribed",  }
                    }
    
            elif self.channel == 'sms':
                tp = "SMS"
                token= f"+{self.phone_number}" if not self.phone_number.startswith("+") else self.phone_number
                payload = {
                    "properties": {"ip":self.ip},
                    "subscriptions":[   {"type": tp,"token":token,"enabled":True}  ],
                    "tags": {  "subscription_status": "subscribed",  }
                    } 
            else:
                _logger.error("Invalid notification type specified")
                return
            
            
            if self.external_id:
                payload["identity"] = {"external_id": self.external_id}
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
       
    
    
    
    
    def delete_user(self):
        for rec in self:
            app_id=rec.app_id
            api_key=rec.api_key
            _logger.info(f"player app_id....................................{app_id}")
            _logger.info(f"player api_key....................................{api_key}")
            
            url = f"https://onesignal.com/api/v1/players/{rec.player_id}?app_id={app_id}"

            headers = {
                "accept": "application/json",
                "Authorization": f"Basic {api_key}"
            }

            response = requests.delete(url, headers=headers)
            if response.status_code == 200:
                self.unlink()
                _logger.info("success=================================================SUCCESS===========================")
            else:
                    _logger.error(f"User creation failed: {response.status_code}, {response.text}")
            
            _logger.info(f"user deleted ..........................................{response}")
        return