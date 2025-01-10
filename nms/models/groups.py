from odoo import fields,api,models 

class ResGroups(models.Model):
    _inherit='res.groups'
    # def get_application_groups(self,domain):
    #     group_id=self.env.ref('base.view_groups_form').id
    #     wave_group_id=self.env.ref('stock.group_stock_picking_wave').id 
    #     return super(ResGroups,self).get_application_groups(domain = [('id','not in',[group_id,wave_group_id])])
        
        
    def get_application_groups(self, domain):
        group_id = self.env.ref('account.group_sale_receipts').id
        return super(ResGroups, self).get_application_groups(domain+[('id','!=',group_id)])
