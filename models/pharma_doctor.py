from odoo import api, fields, models

class PharmaDoctor(models.Model):
    _name = 'pharma.doctor'
    _description = 'Doctor Information'

    name = fields.Char(string='Name', required=True)
    specialization = fields.Char(string='Specialization')
    phone = fields.Char(string='Phone')
    email = fields.Char(string='Email')
    city = fields.Char(string='City')

    # One2many to link prescriptions
    prescription_ids = fields.One2many(
        'pharma.prescription', 'doctor_id', string='Prescriptions'
    )

    # Computed field for smart button
    prescription_count = fields.Integer(
        string='Prescription Count', compute='_compute_prescription_count'
    )

    # Compute method for prescription_count
    def _compute_prescription_count(self):
        for doctor in self:
            doctor.prescription_count = len(doctor.prescription_ids)

    # Smart button to open related prescriptions
    def action_open_prescriptions(self):
        return {
            'type': 'ir.actions.act_window',
            'name': 'Prescriptions',
            'res_model': 'pharma.prescription',
            'view_mode': 'tree,form',
            'domain': [('doctor_id', '=', self.id)],
            'context': {'default_doctor_id': self.id},
        }

    def print_doctor_report(self):
        """Generate PDF report for the selected doctor."""
        return self.env.ref('pharma_management.report_pharma_doctor').report_action(self)
