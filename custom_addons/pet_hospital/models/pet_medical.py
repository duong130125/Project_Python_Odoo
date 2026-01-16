from odoo import models, fields, api
from odoo.exceptions import ValidationError

class PetVaccination(models.Model):
    _name = 'pet.vaccination'
    _description = 'Pet Vaccination'

    name = fields.Char(string='Vaccine Name', required=True)
    date = fields.Date(string='Date', required=True, default=fields.Date.context_today)
    next_date = fields.Date(string='Next Date')
    pet_id = fields.Many2one('pet.pet', string='Pet', required=True, ondelete='cascade')

    @api.constrains('date', 'next_date')
    def _check_dates(self):
        for record in self:
            if record.date > fields.Date.today():
                raise ValidationError("Vaccination date cannot be in the future!")
            if record.next_date and record.date and record.next_date <= record.date:
                raise ValidationError("Next vaccination date must be after the current vaccination date!")

class PetMedicalHistory(models.Model):
    _name = 'pet.medical.history'
    _description = 'Medical History'
    _rec_name = 'diagnosis'

    date = fields.Date(string='Date', required=True, default=fields.Date.context_today)
    doctor_id = fields.Many2one('res.partner', string='Doctor')
    diagnosis = fields.Char(string='Diagnosis', required=True)
    description = fields.Text(string='Description')
    pet_id = fields.Many2one('pet.pet', string='Pet', required=True, ondelete='cascade')
