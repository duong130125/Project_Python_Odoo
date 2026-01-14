from odoo import models, fields

class PetType(models.Model):
    _name = 'pet.type'
    _description = 'Pet Type'

    name = fields.Char(required=True)
    breed_ids = fields.One2many('pet.breed', 'type_id', string="Breeds")


class PetBreed(models.Model):
    _name = 'pet.breed'
    _description = 'Pet Breed'

    name = fields.Char(required=True)
    type_id = fields.Many2one('pet.type', string="Pet Type", required=True)
