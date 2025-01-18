from odoo import fields,api,models 

class ResGroups(models.Model):
    _inherit='res.groups'
    
    def get_application_groups(self, domain):
        wave_group_id = self.env.ref('stock.group_stock_picking_wave').id
        return super(ResGroups, self).get_application_groups(domain+[('id','!=',wave_group_id)])
