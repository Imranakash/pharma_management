from odoo import api, fields, models
from odoo.exceptions import ValidationError

class PharmaRepresentative(models.Model):
    _name = 'pharma.representative'
    _description = 'Medical Representative'

    name = fields.Char(string='Name', required=True)
    employee_id = fields.Char(string='Employee ID', required=True)
    target_value = fields.Float(string='Target Value')
    region = fields.Char(string='Region')
    phone = fields.Char(string='Phone')

    # user_id = fields.Many2one(
    #     'res.users',
    #     string='Related User',
    #     help='The system user linked to this representative.'
    # )

    total_sales = fields.Float(
        string='Total Sales',
        compute='_compute_total_sales',
        store=True
    )
    achievement_rate = fields.Float(
        string='Achievement Rate (%)',
        compute='_compute_achievement_rate',
        store=True
    )

    state = fields.Selection(
        [('active', 'Active'), ('inactive', 'Inactive')],
        string='Status',
        default='active'
    )

    _sql_constraints = [
        ('employee_id_unique', 'unique(employee_id)', 'Employee ID must be unique!'),
    ]

    # === COMPUTE METHODS ===
    @api.depends()  # no depends because prescription model not yet defined
    def _compute_total_sales(self):
        """Placeholder computation until prescription model is added."""
        for rep in self:
            rep.total_sales = 0.0  # later you can sum related prescriptions

    @api.depends('total_sales', 'target_value')
    def _compute_achievement_rate(self):
        for rep in self:
            if rep.target_value > 0:
                rep.achievement_rate = (rep.total_sales / rep.target_value) * 100
            else:
                rep.achievement_rate = 0.0

    # === CONSTRAINTS ===
    @api.constrains('target_value')
    def _check_target_value(self):
        for rec in self:
            if rec.target_value < 0:
                raise ValidationError("Target value cannot be negative.")
