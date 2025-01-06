# -*- coding: utf-8 -*-
# from odoo import http


# class Nms(http.Controller):
#     @http.route('/nms/nms', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/nms/nms/objects', auth='public')
#     def list(self, **kw):
#         return http.request.render('nms.listing', {
#             'root': '/nms/nms',
#             'objects': http.request.env['nms.nms'].search([]),
#         })

#     @http.route('/nms/nms/objects/<model("nms.nms"):obj>', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('nms.object', {
#             'object': obj
#         })

