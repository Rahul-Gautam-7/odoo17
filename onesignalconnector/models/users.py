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
    
    
    @api.model
    def create_user_in_onesignal(self,app_id):
                signal_records = self.env['signal.connect'].search([],limit=1)  # Modify this search as needed
                url = f"https://api.onesignal.com/apps/{signal_records.app_id}/users"
                _logger.info(f"================================================={signal_records.app_id}")
                # You can set up additional fields you want to pass to the OneSignal API
                _logger.info(f"=============================={self.ip}")
                payload = {
                    "properties": {
                        "ip":self.ip,
                    },
                "identity": { "external_id": "test_external_id" }
                }
                headers = {
                    "Authorization": f"Basic {signal_records.api_key}",
                    "Content-Type": "application/json",
                }
            
                try:
                    # Make the API request to OneSignal
                    response = requests.post(url, headers=headers, json=payload)
                
                    if response.status_code == 200:
                        _logger.info("User creation successful in OneSignal.")
                        data = response.json()
                        player_id = data.get("id")
                        device_type = data.get("device_type")
                    
                        # Handle device type logic for WebPush or SMS
                        if device_type == 5:  # WebPush
                            _logger.info("Creating user as WebPush.")
                        elif device_type == 2:  # SMS
                            _logger.info("Creating user as SMS.")
                        else:
                            _logger.info(f"Unknown device_type {device_type}.")
                    
                        # Create the user.fetch record in Odoo
                        self.env['user.fetch'].create({
                            'connector_ids': signal_record.id,
                            'player_id': player_id,
                            'created_at': datetime.utcnow(),
                        })
                    else:
                        _logger.error(f"User creation failed: {response.status_code}, {response.text}")
                except requests.exceptions.RequestException as e:
                    _logger.error(f"Error creating user in OneSignal: {str(e)}")
       


