from odoo import models, fields, api
from odoo.exceptions import ValidationError
from datetime import date
from dateutil.relativedelta import relativedelta

class PetPet(models.Model):
    _name = 'pet.pet'
    _description = 'Pet'

    name = fields.Char(string="Pet Name", required=True)
    code = fields.Char(string="Code", required=True, copy=False, readonly=True, default='New')
    image = fields.Image(string="Image")

    dob = fields.Date(string="Date of Birth")
    age = fields.Integer(string="Age", compute="_compute_age", store=True)

    owner_id = fields.Many2one(
        'res.partner',
        string="Owner",
        ondelete='set null'
    )

    owner_phone = fields.Char(string="Owner Phone", related="owner_id.phone", readonly=True, store=True)
    owner_address = fields.Char(string="Owner Address", related="owner_id.contact_address", readonly=True, store=True)

    type_id = fields.Many2one('pet.type', string="Type")
    breed_id = fields.Many2one('pet.breed', string="Breed", domain="[('type_id', '=', type_id)]")

    vaccination_ids = fields.One2many('pet.vaccination', 'pet_id', string="Vaccinations")
    medical_history_ids = fields.One2many('pet.medical.history', 'pet_id', string="Medical History")
    medical_count = fields.Integer(compute='_compute_medical_count', string="Medical Count")

    booking_ids = fields.One2many('pet.booking', 'pet_id', string="Bookings")
    booking_count = fields.Integer(compute='_compute_booking_count', string="Booking Count")
    spa_count = fields.Integer(string="Spa Count", readonly=True, default=0)

    _sql_constraints = [
        ('code_unique', 'unique(code)', 'The Pet Code must be unique!')
    ]

    @api.model
    def create(self, vals):
        if vals.get('code', 'New') == 'New':
            vals['code'] = self.env['ir.sequence'].next_by_code('pet.pet') or 'New'
        return super(PetPet, self).create(vals)

    def _compute_medical_count(self):
        for pet in self:
            pet.medical_count = len(pet.medical_history_ids)

    def _compute_booking_count(self):
        for pet in self:
            pet.booking_count = len(pet.booking_ids)

    def action_view_medical_history(self):
        self.ensure_one()
        return {
            'name': 'Medical History',
            'type': 'ir.actions.act_window',
            'res_model': 'pet.medical.history',
            'view_mode': 'tree,form',
            'domain': [('pet_id', '=', self.id)],
            'context': {'default_pet_id': self.id},
        }

    def action_view_bookings(self):
        self.ensure_one()
        return {
            'name': 'Bookings',
            'type': 'ir.actions.act_window',
            'res_model': 'pet.booking',
            'view_mode': 'tree,form',
            'domain': [('pet_id', '=', self.id)],
            'context': {'default_pet_id': self.id},
        }

    @api.depends('dob')
    def _compute_age(self):
        for pet in self:
            if pet.dob:
                today = date.today()
                pet.age = relativedelta(today, pet.dob).years
            else:
                pet.age = 0


    @api.constrains('dob')
    def _check_dob(self):
        today = fields.Date.today()
        for pet in self:
            if pet.dob and pet.dob > today:
                raise ValidationError("Date of birth cannot be in the future!")
