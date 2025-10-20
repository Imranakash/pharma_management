from odoo import api, fields, models
from odoo.exceptions import ValidationError

class PharmaMedicine(models.Model):
    _name = 'pharma.medicine'
    _description = 'Medicine Catalog'

    name = fields.Char(string='Medicine Name', required=True)
    code = fields.Char(string='Medicine Code', required=True)
    category = fields.Selection([
        ('tablet', 'Tablet'),
        ('syrup', 'Syrup'),
        ('injection', 'Injection'),
        ('capsule', 'Capsule'),
        ('other', 'Other')
    ], string='Category', required=True)
    price = fields.Float(string='Price', required=True)
    stock_qty = fields.Integer(string='Stock Quantity', default=0)

    # Computed field for low stock warning
    is_low_stock = fields.Boolean(
        string='Low Stock',
        compute='_compute_is_low_stock',
        store=True
    )

    _sql_constraints = [
        ('code_unique', 'unique(code)', 'Medicine Code must be unique!'),
    ]

    # === COMPUTE METHODS ===
    @api.depends('stock_qty')
    def _compute_is_low_stock(self):
        for med in self:
            med.is_low_stock = med.stock_qty < 10

    # === CONSTRAINTS ===
    @api.constrains('stock_qty')
    def _check_stock_qty(self):
        for med in self:
            if med.stock_qty < 0:
                raise ValidationError("Stock quantity cannot be negative.")
