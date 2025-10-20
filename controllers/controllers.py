# -*- coding: utf-8 -*-
# from odoo import http


# class PharmaManagement(http.Controller):
#     @http.route('/pharma_management/pharma_management', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/pharma_management/pharma_management/objects', auth='public')
#     def list(self, **kw):
#         return http.request.render('pharma_management.listing', {
#             'root': '/pharma_management/pharma_management',
#             'objects': http.request.env['pharma_management.pharma_management'].search([]),
#         })

#     @http.route('/pharma_management/pharma_management/objects/<model("pharma_management.pharma_management"):obj>', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('pharma_management.object', {
#             'object': obj
#         })

