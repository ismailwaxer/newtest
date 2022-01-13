# -*- coding: utf-8 -*-
# from odoo import http


# class QuotationApporval(http.Controller):
#     @http.route('/quotation_apporval/quotation_apporval/', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/quotation_apporval/quotation_apporval/objects/', auth='public')
#     def list(self, **kw):
#         return http.request.render('quotation_apporval.listing', {
#             'root': '/quotation_apporval/quotation_apporval',
#             'objects': http.request.env['quotation_apporval.quotation_apporval'].search([]),
#         })

#     @http.route('/quotation_apporval/quotation_apporval/objects/<model("quotation_apporval.quotation_apporval"):obj>/', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('quotation_apporval.object', {
#             'object': obj
#         })
