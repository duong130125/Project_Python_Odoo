from odoo import models, fields, api, _
from odoo.exceptions import ValidationError, UserError
from datetime import date

class PetBooking(models.Model):
    _name = 'pet.booking'
    _description = 'Pet Booking'
    _inherit = ['mail.thread', 'mail.activity.mixin']

    name = fields.Char(string='Booking Reference', required=True, copy=False, readonly=True, default='New')
    partner_id = fields.Many2one('res.partner', string='Customer', required=True)
    pet_id = fields.Many2one('pet.pet', string='Pet', required=True, domain="[('owner_id', '=', partner_id)]")
    booking_date = fields.Date(string='Booking Date', required=True, default=fields.Date.context_today)
    
    booking_line_ids = fields.One2many('pet.booking.line', 'booking_id', string='Order Lines')
    amount_total = fields.Monetary(string='Total', store=True, readonly=True, compute='_compute_amount')
    currency_id = fields.Many2one('res.currency', string='Currency', related='company_id.currency_id')
    company_id = fields.Many2one('res.company', string='Company', default=lambda self: self.env.company)

    state = fields.Selection([
        ('draft', 'Draft'),
        ('confirmed', 'Confirmed'),
        ('in_progress', 'In Progress'),
        ('done', 'Done'),
        ('cancel', 'Cancelled'),
    ], string='Status', readonly=True, default='draft', tracking=True)

    @api.model
    def create(self, vals):
        if vals.get('name', 'New') == 'New':
            vals['name'] = self.env['ir.sequence'].next_by_code('pet.booking') or 'New'
        return super(PetBooking, self).create(vals)

    def action_confirm(self):
        self.write({'state': 'confirmed'})

    def action_start_work(self):
        self.write({'state': 'in_progress'})

    def action_done(self):
        for booking in self:
            booking.write({'state': 'done'})
            if booking.pet_id:
                booking.pet_id.spa_count += 1

    def action_cancel(self):
        for booking in self:
            if booking.state != 'draft':
                raise UserError(_("Only Draft bookings can be cancelled!"))
            booking.write({'state': 'cancel'})

    def action_draft(self):
        self.write({'state': 'draft'})

    @api.depends('booking_line_ids.price_subtotal')
    def _compute_amount(self):
        for order in self:
            order.amount_total = sum(line.price_subtotal for line in order.booking_line_ids)

    @api.constrains('booking_date')
    def _check_booking_date(self):
        for record in self:
            if record.booking_date and record.booking_date < date.today():
                raise ValidationError("Booking date cannot be in the past!")

    @api.onchange('partner_id')
    def _onchange_partner_id(self):
        self.pet_id = False
        if self.partner_id:
            return {'domain': {'pet_id': [('owner_id', '=', self.partner_id.id)]}}
        return {'domain': {'pet_id': []}}


class PetBookingLine(models.Model):
    _name = 'pet.booking.line'
    _description = 'Booking Line'

    booking_id = fields.Many2one('pet.booking', string='Booking Reference', required=True, ondelete='cascade', index=True, copy=False)
    product_id = fields.Many2one('product.product', string='Service', required=True, domain="[('is_pet_service', '=', True)]")
    name = fields.Text(string='Description')
    product_uom_qty = fields.Float(string='Quantity', default=1.0, required=True)
    price_unit = fields.Float(string='Unit Price', required=True, digits='Product Price')
    price_subtotal = fields.Monetary(compute='_compute_amount', string='Subtotal', readonly=True, store=True)
    currency_id = fields.Many2one(related='booking_id.currency_id', depends=['booking_id.currency_id'], store=True, string='Currency', readonly=True)

    @api.depends('product_uom_qty', 'price_unit')
    def _compute_amount(self):
        for line in self:
            line.price_subtotal = line.product_uom_qty * line.price_unit

    @api.onchange('product_id')
    def _onchange_product_id(self):
        if self.product_id:
            self.price_unit = self.product_id.list_price
            self.name = self.product_id.name

    @api.constrains('product_uom_qty')
    def _check_qty(self):
        for line in self:
            if line.product_uom_qty <= 0:
                raise ValidationError("Quantity must be greater than 0.")
