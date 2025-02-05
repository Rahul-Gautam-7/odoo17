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
    
    player_id=fields.Char(string="Player Id")
    connector_ids=fields.Many2one('signal.connect',string="Name",ondelete='cascade')

    app_id=fields.Char(related='connector_ids.app_id',store=True)
    api_key=fields.Char(related="connector_ids.api_key",store=True)
    

    identifier = fields.Char(string="Identifier")
    session_count = fields.Integer(string="Session Count")
    language = fields.Char(string="Language")
    timezone = fields.Integer(string="Time Zone")
    game_version = fields.Char(string="Game Version")
    device_os = fields.Char(string="Device OS")
    device_type = fields.Char(string="Device Type")
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
                            identifier = player.get('identifier')
                            session_count = player.get('session_count', 0)
                            language = player.get('language')
                            timezone = player.get('timezone', 0)
                            game_version = player.get('game_version', '')
                            device_os = player.get('device_os', '')
                            device_type = DEVICE_TYPE_MAPPING.get(player.get('device_type'))
                            device_model = player.get('device_model', '')
                            ad_id = player.get('ad_id', '')
                            last_active = datetime.utcfromtimestamp(player.get('last_active'))
                            playtime = player.get('playtime', 0.0)
                            amount_spent = player.get('amount_spent', 0.0)
                            created_at = datetime.utcfromtimestamp(player.get('created_at'))
                            invalid_identifier = player.get('invalid_identifier', False)
                            sdk = player.get('sdk', '')
                            test_type = player.get('test_type', None)
                            ip = player.get('ip', '')
                            tags = player.get('tags', {})

                            existing_player = self.env['user.fetch'].search([
                                ('connector_ids', '=', record.id),
                                ('player_id', '=', player_id)
                            ], limit=1)
                        
                            if not existing_player:
                                self.env['user.fetch'].create({
                                    'connector_ids': record.id,
                                    'player_id': player_id,
                                    'identifier': identifier,
                                    'session_count': session_count,
                                    'language': language,
                                    'timezone': timezone,
                                    'game_version': game_version,
                                    'device_os': device_os,
                                    'device_type': device_type,
                                    'device_model': device_model,
                                    'ad_id': ad_id,
                                    'last_active': last_active,
                                    'playtime': playtime,
                                    'amount_spent': amount_spent,
                                    'created_at': created_at,
                                    'invalid_identifier': invalid_identifier,
                                    'sdk': sdk,
                                    'test_type': test_type,
                                    'ip': ip,
                                    'tags': str(tags)  # Storing tags as a string (JSON format)
                                })
                            else:
                                _logger.info(f"Player {player_id} already exists.")
                    else:
                        _logger.info("User Fetch Failure")
                except requests.exceptions.RequestException as e:
                    _logger.info("Error in sending notifiy",str(e))