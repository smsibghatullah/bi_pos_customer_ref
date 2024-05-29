# -*- coding: utf-8 -*-
# from odoo import http


# class PosCustomization(http.Controller):
#     @http.route('/pos_customization/pos_customization', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/pos_customization/pos_customization/objects', auth='public')
#     def list(self, **kw):
#         return http.request.render('pos_customization.listing', {
#             'root': '/pos_customization/pos_customization',
#             'objects': http.request.env['pos_customization.pos_customization'].search([]),
#         })

#     @http.route('/pos_customization/pos_customization/objects/<model("pos_customization.pos_customization"):obj>', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('pos_customization.object', {
#             'object': obj
#         })
