from odoo import api,fields,models

class OWlTodo(models.Model):
    _name="owl.todo.list"
    _description="Todo list in owljs odoo"

    name=fields.Char(string="Task Name")
    completed=fields.Boolean()
    color = fields.Char()