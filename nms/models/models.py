# -*- coding: utf-8 -*-

from odoo import models, fields, api


class Saless(models.Model):

    _inherit = 'product.template'
    _description = 'nms.nms'

    inherit_name = fields.Char("Inherited field")

    def action_update_quantity_on_hand(self):
        super(Saless,self).action_update_quantity_on_hand()
        self.inherit_name=self.name

