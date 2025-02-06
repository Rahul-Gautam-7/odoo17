from odoo import api,fields,models
import requests
import logging

_logger=logging.getLogger(__name__)

class User(models.Model):
    _name="user.fetch"
    _description="Fetching users"
    _rec_name="player_id"
    
    player_id=fields.Char(string="Player Id")
    connector_ids=fields.Many2one('signal.connect',string="Name")

    app_id=fields.Char(related='connector_ids.app_id',store=True)
    api_key=fields.Char(related="connector_ids.api_key",store=True)
    


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
                        for users in data.get('players',[]):
                            player_id = users.get('id')
                            existing_field=self.env['user.fetch'].search([
                                ('connector_ids','=',record.id),
                                ('player_id','=',player_id)
                            ],limit=1)
                            
                            if not existing_field:
                                self.env['user.fetch'].create({
                                    'connector_ids':record.id,
                                    'player_id':player_id,
                                    
                                })
                    else:
                        _logger.info("User Fetch Failure")
                except requests.exceptions.RequestException as e:
                    _logger.info("Error in sending notifiy",str(e))