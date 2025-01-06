# -*- coding: utf-8 -*-
# from odoo import http


# class OdooInherit(http.Controller):
#     @http.route('/odoo_inherit/odoo_inherit', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/odoo_inherit/odoo_inherit/objects', auth='public')
#     def list(self, **kw):
#         return http.request.render('odoo_inherit.listing', {
#             'root': '/odoo_inherit/odoo_inherit',
#             'objects': http.request.env['odoo_inherit.odoo_inherit'].search([]),
#         })

#     @http.route('/odoo_inherit/odoo_inherit/objects/<model("odoo_inherit.odoo_inherit"):obj>', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('odoo_inherit.object', {
#             'object': obj
#         })

