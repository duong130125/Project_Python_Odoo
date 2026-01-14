from odoo import models, fields

class ResPartner(models.Model):
    _inherit = 'res.partner'

    pet_ids = fields.One2many(
        'pet.pet',
        'owner_id',
        string="Pets"
    )
    pet_count = fields.Integer(compute='_compute_pet_count', string="Pet Count")

    def _compute_pet_count(self):
        for partner in self:
            partner.pet_count = len(partner.pet_ids)

    def action_view_pets(self):
        self.ensure_one()
        return {
            'name': 'Pets',
            'type': 'ir.actions.act_window',
            'res_model': 'pet.pet',
            'view_mode': 'tree,form',
            'domain': [('owner_id', '=', self.id)],
            'context': {'default_owner_id': self.id},
        }
