# -*- coding: utf-8 -*-
# from odoo import http


# class PetHospital(http.Controller):
#     @http.route('/pet_hospital/pet_hospital', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/pet_hospital/pet_hospital/objects', auth='public')
#     def list(self, **kw):
#         return http.request.render('pet_hospital.listing', {
#             'root': '/pet_hospital/pet_hospital',
#             'objects': http.request.env['pet_hospital.pet_hospital'].search([]),
#         })

#     @http.route('/pet_hospital/pet_hospital/objects/<model("pet_hospital.pet_hospital"):obj>', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('pet_hospital.object', {
#             'object': obj
#         })

