from odoo import models, fields, api
from odoo.exceptions import ValidationError, UserError

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

    def action_confirm(self):
        self.write({'state': 'confirmed'})

    def action_done(self):
        self.write({'state': 'done'})

    def action_cancel(self):
        self.write({'state': 'cancel'})

    @api.model
    def create(self, vals):
        if vals.get('name', 'New') == 'New':
            vals['name'] = self.env['ir.sequence'].next_by_code('pet.appointment') or 'New'
        return super(PetAppointment, self).create(vals)

    @api.constrains('date_start', 'date_end')
    def _check_dates(self):
        for record in self:
            if record.date_start and record.date_end:
                 if record.date_start >= record.date_end:
                    raise ValidationError("End Date must be after Start Date!")
                 if record.date_start < fields.Datetime.now():
                    raise ValidationError("Appointment cannot be in the past!")
                 
                 domain = [
                     ('id', '!=', record.id),
                     ('pet_id', '=', record.pet_id.id),
                     ('state', '!=', 'cancel'),
                     ('date_start', '<', record.date_end),
                     ('date_end', '>', record.date_start),
                 ]
                 if self.search_count(domain) > 0:
                     raise ValidationError("This pet already has an appointment during this time!")

    def unlink(self):
        for appointment in self:
            if appointment.state == 'done':
                raise UserError("You cannot delete an appointment that is already Done.")
        return super(PetAppointment, self).unlink()
