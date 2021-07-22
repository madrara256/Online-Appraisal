# -*- coding: utf-8 -*-
from odoo import http

# class Pmt(http.Controller):
#     @http.route('/pmt/pmt/', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/pmt/pmt/objects/', auth='public')
#     def list(self, **kw):
#         return http.request.render('pmt.listing', {
#             'root': '/pmt/pmt',
#             'objects': http.request.env['pmt.pmt'].search([]),
#         })

#     @http.route('/pmt/pmt/objects/<model("pmt.pmt"):obj>/', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('pmt.object', {
#             'object': obj
#         })