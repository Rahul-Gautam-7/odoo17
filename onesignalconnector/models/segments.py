from odoo import api,fields,models
import requests
import logging

_logger = logging.getLogger(__name__)

class Segments(models.Model):
    _name="onesignal.segment"
    _description="One signal segments"
    
    name=fields.Char(string="Segment Name")
    seg_id=fields.Char(string="Segment Id")
    connector_ids=fields.Many2one('signal.connect',string="Segment ID")
    app_id=fields.Char(related="connector_ids.app_id",store=True)
    api_key=fields.Char(related="connector_ids.api_key",store=True)
    
    
    @api.model
    def check_segments(self,app_id):
        signal_rec = self.env['signal.connect'].search([('id','=',app_id)])
        for record in signal_rec:
            app_id=record.app_id
            api_key=record.api_key
            if app_id:
                url=f"https://api.onesignal.com/apps/{app_id}/segments?offset=0&limit=300"
                
                headers={
                    'Authorization':f"Basic {api_key}",
                    'Content-Type':'application/json',
                }
                try:
                    response = requests.get(url,headers=headers)
                    _logger.info(response)
                    if response.status_code == 200:
                        data = response.json()
                        for segmentss in data.get('segments',[]):
                            seg_id=segmentss.get('id')
                            existing_segments=self.env['onesignal.segment'].search([
                                ('connector_ids','=',record.id),
                                ('seg_id','=',seg_id)
                            ],limit=1)
                            
                            if not existing_segments:
                                self.env['onesignal.segment'].create({
                                    'connector_ids':record.id,
                                    'seg_id':seg_id,
                                    'name':segmentss.get('name')
                                })
                            else:
                                _logger.info("Segment not fetched")
                except requests.exceptions.RequestException as e:
                    _logger.info("Error in sending notifiy",str(e))
                            
                            
    