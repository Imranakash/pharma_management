from odoo import api, fields, models

class PharmaPrescriptionLine(models.Model):
    _name = 'pharma.prescription.line'
    _description = 'Prescription Medicine Line'

    prescription_id = fields.Many2one('pharma.prescription', string='Prescription', ondelete='cascade')
    medicine_id = fields.Many2one('pharma.medicine', string='Medicine', required=True)
    quantity = fields.Integer(string='Quantity', required=True)
    price_unit = fields.Float(related='medicine_id.price', string='Unit Price', store=True)
    subtotal = fields.Float(string='Subtotal', compute='_compute_subtotal', store=True)

    @api.depends('quantity', 'price_unit')
    def _compute_subtotal(self):
        for line in self:
            line.subtotal = line.quantity * line.price_unit
