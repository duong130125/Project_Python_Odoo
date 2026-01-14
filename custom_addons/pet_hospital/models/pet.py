from odoo import models, fields, api
from datetime import date

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

    owner_phone = fields.Char(string="Owner Phone")
    owner_address = fields.Char(string="Owner Address")

    type_id = fields.Many2one('pet.type', string="Type")
    breed_id = fields.Many2one('pet.breed', string="Breed")

    vaccination_ids = fields.One2many('pet.vaccination', 'pet_id', string="Vaccinations")
    medical_history_ids = fields.One2many('pet.medical.history', 'pet_id', string="Medical History")
    medical_count = fields.Integer(compute='_compute_medical_count', string="Medical Count")

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

    @api.depends('dob')
    def _compute_age(self):
        for pet in self:
            if pet.dob:
                today = date.today()
                pet.age = today.year - pet.dob.year - (
                    (today.month, today.day) < (pet.dob.month, pet.dob.day)
                )
            else:
                pet.age = 0

    @api.onchange('owner_id')
    def _onchange_owner_id(self):
        if self.owner_id:
            self.owner_phone = self.owner_id.phone
            self.owner_address = self.owner_id.contact_address
