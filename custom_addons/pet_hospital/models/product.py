from odoo import models, fields

class ProductTemplate(models.Model):
    _inherit = 'product.template'

    is_pet_service = fields.Boolean(string="Is Pet Service")
