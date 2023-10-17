# -*- coding: utf-8 -*-
# from odoo import http


# class HideSaleMargin(http.Controller):
#     @http.route('/hide_sale_margin/hide_sale_margin/', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/hide_sale_margin/hide_sale_margin/objects/', auth='public')
#     def list(self, **kw):
#         return http.request.render('hide_sale_margin.listing', {
#             'root': '/hide_sale_margin/hide_sale_margin',
#             'objects': http.request.env['hide_sale_margin.hide_sale_margin'].search([]),
#         })

#     @http.route('/hide_sale_margin/hide_sale_margin/objects/<model("hide_sale_margin.hide_sale_margin"):obj>/', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('hide_sale_margin.object', {
#             'object': obj
#         })
