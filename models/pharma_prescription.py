from odoo import api, fields, models
from odoo.exceptions import ValidationError

class PharmaPrescription(models.Model):
    _name = 'pharma.prescription'
    _description = 'Prescription Management'
    _inherit = ['mail.thread', 'mail.activity.mixin']

    doctor_id = fields.Many2one(
        'pharma.doctor',
        string='Doctor',
        required=True,
        tracking=True
    )
    representative_id = fields.Many2one(
        'pharma.representative',
        string='Representative',
        required=True,
        tracking=True
    )
    prescription_date = fields.Date(
        string='Prescription Date',
        required=True,
        default=fields.Date.context_today,
        tracking=True
    )
    medicine_line_ids = fields.One2many(
        'pharma.prescription.line',
        'prescription_id',
        string='Medicines',
        tracking=True
    )
    total_amount = fields.Float(
        string='Total Amount',
        compute='_compute_total_amount',
        store=True,
        tracking=True
    )
    state = fields.Selection([
        ('draft', 'Draft'),
        ('confirmed', 'Confirmed'),
        ('cancelled', 'Cancelled'),
    ], string='Status', default='draft', tracking=True)

    # === COMPUTE TOTAL ===
    @api.depends('medicine_line_ids.subtotal')
    def _compute_total_amount(self):
        for rec in self:
            rec.total_amount = sum(line.subtotal for line in rec.medicine_line_ids)

    # === ACTION METHODS ===
    def action_confirm(self):
        """Confirm the prescription and safely reduce stock quantities."""
        for rec in self:
            if not rec.medicine_line_ids:
                raise ValidationError(
                    "Please add at least one medicine line before confirming."
                )
            for line in rec.medicine_line_ids:
                medicine = line.medicine_id
                if line.quantity > medicine.stock_qty:
                    raise ValidationError(
                        f"Not enough stock for {medicine.name}! "
                        f"Available: {medicine.stock_qty}, Required: {line.quantity}"
                    )
                # ORM-safe stock update
                medicine.write({'stock_qty': medicine.stock_qty - line.quantity})
            rec.state = 'confirmed'

    def action_cancel(self):
        """Cancel the prescription."""
        self.state = 'cancelled'

    def action_reset_draft(self):
        """Reset prescription back to draft."""
        self.state = 'draft'
