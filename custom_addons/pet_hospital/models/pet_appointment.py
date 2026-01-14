from odoo import models, fields, api

class PetAppointment(models.Model):
    _name = 'pet.appointment'
    _description = 'Pet Appointment'

    name = fields.Char(string='Appointment ID', required=True, copy=False, readonly=True, default='New')
    pet_id = fields.Many2one('pet.pet', string='Pet', required=True)
    partner_id = fields.Many2one('res.partner', string='Owner', related='pet_id.owner_id', store=True, readonly=True)
    date_start = fields.Datetime(string='Start Time', required=True)
    date_end = fields.Datetime(string='End Time', required=True)
    description = fields.Text(string='Description')
    state = fields.Selection([
        ('draft', 'Draft'),
        ('confirmed', 'Confirmed'),
        ('done', 'Done'),
        ('cancel', 'Cancelled'),
    ], string='Status', default='draft')

    @api.model
    def create(self, vals):
        if vals.get('name', 'New') == 'New':
            vals['name'] = self.env['ir.sequence'].next_by_code('pet.appointment') or 'New'
        return super(PetAppointment, self).create(vals)
