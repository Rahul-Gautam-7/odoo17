from odoo import fields,models,api

class TestModel(models.Model):
    _name='test.module'
    _description="Module made for testing purpose"

    name=fields.Char(string="Test Name")