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
   
    
    
    
    
    
    @api.model
    def check_templates(self):
        signal_rec = self.env['signal.connect'].search([])
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
                        for templatess in data.get('templates',[]):
                            _logger.info(f"Fetched template: {templatess}")
                            temps_id=templatess.get('id')
                            existing_segments=self.env['onesignal.template'].search([
                                ('connector_ids','=',record.id),
                                ('temps_id','=',temps_id),
                            ],limit=1)
                            
                            if not existing_segments:
                                self.env['onesignal.template'].create({
                                    'connector_ids':record.id,
                                    'temps_id':temps_id,
                                    'name':templatess.get('name'),
                                    'channel':templatess.get('channel'),
                                })
                            else:
                                _logger.info("Segment not fetched")
                except requests.exceptions.RequestException as e:
                    _logger.info("Error in sending notifiy",str(e))
                            
                            
    