from odoo import models, fields

class PetVaccination(models.Model):
    _name = 'pet.vaccination'
    _description = 'Pet Vaccination'

    name = fields.Char(string='Vaccine Name', required=True)
    date = fields.Date(string='Date', required=True, default=fields.Date.context_today)
    next_date = fields.Date(string='Next Date')
    pet_id = fields.Many2one('pet.pet', string='Pet', required=True, ondelete='cascade')

class PetMedicalHistory(models.Model):
    _name = 'pet.medical.history'
    _description = 'Medical History'

    date = fields.Date(string='Date', required=True, default=fields.Date.context_today)
    doctor_id = fields.Many2one('res.partner', string='Doctor')
    diagnosis = fields.Char(string='Diagnosis', required=True)
    description = fields.Text(string='Description')
    pet_id = fields.Many2one('pet.pet', string='Pet', required=True, ondelete='cascade')
