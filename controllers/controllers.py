# -*- coding: utf-8 -*-
from odoo import http

# class LtasquesUi(http.Controller):
#     @http.route('/ltasques_ui/ltasques_ui/', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/ltasques_ui/ltasques_ui/objects/', auth='public')
#     def list(self, **kw):
#         return http.request.render('ltasques_ui.listing', {
#             'root': '/ltasques_ui/ltasques_ui',
#             'objects': http.request.env['ltasques_ui.ltasques_ui'].search([]),
#         })

#     @http.route('/ltasques_ui/ltasques_ui/objects/<model("ltasques_ui.ltasques_ui"):obj>/', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('ltasques_ui.object', {
#             'object': obj
#         })