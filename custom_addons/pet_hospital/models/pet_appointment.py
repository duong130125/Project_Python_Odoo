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
    @api.model
    def _expand_states(self, states, domain, order):
        return [key for key, val in type(self).state.selection]

    state = fields.Selection([
        ('draft', 'Draft'),
        ('confirmed', 'Confirmed'),
        ('done', 'Done'),
        ('cancel', 'Cancelled'),
    ], string='Status', default='draft', group_expand='_expand_states')

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
        
        res = super(PetAppointment, self).create(vals)

        if res.date_start and res.date_start < fields.Datetime.now():
            res.action_confirm()
            res.action_done()
            
        return res

    @api.constrains('date_start', 'date_end')
    def _check_dates(self):
        for record in self:
            if record.date_start and record.date_end:
                 if record.date_start >= record.date_end:
                    raise ValidationError("End Date must be after Start Date!")
                 
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
            if appointment.state in ['done', 'cancel']:
                raise UserError("You cannot delete an appointment that is already Done or Cancelled.")
        return super(PetAppointment, self).unlink()

    def write(self, vals):
        for record in self:
            if record.state in ['done', 'cancel']:
                 raise UserError("You cannot modify an appointment that is already Done or Cancelled.")
        
        if 'state' in vals:
            target_state = vals['state']
            for record in self:
                if record.state == 'draft' and target_state == 'done':
                    raise UserError("You cannot skip the confirmation step. Please confirm the appointment first.")
                    
        return super(PetAppointment, self).write(vals)
