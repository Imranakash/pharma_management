from odoo import api, fields, models

class PharmaWizardPrescription(models.TransientModel):
    _name = 'pharma.wizard.prescription'
    _description = 'Prescription Creation Assistant'

    doctor_ids = fields.Many2many('pharma.doctor', string='Doctors', required=True)
    representative_id = fields.Many2one('pharma.representative', string='Representative', required=True)
    prescription_date = fields.Date(string='Prescription Date', default=fields.Date.today)
    medicine_id = fields.Many2one('pharma.medicine', string='Medicine', required=True)
    quantity = fields.Integer(string='Quantity', default=1, required=True)

    def action_generate_prescriptions(self):
        """Create prescription records for each selected doctor."""
        Prescription = self.env['pharma.prescription']

        for wizard in self:
            for doctor in wizard.doctor_ids:
                # Create prescription
                prescription = Prescription.create({
                    'doctor_id': doctor.id,
                    'representative_id': wizard.representative_id.id,
                    'prescription_date': wizard.prescription_date,
                    'line_ids': [(0, 0, {
                        'medicine_id': wizard.medicine_id.id,
                        'quantity': wizard.quantity,
                    })]
                })
        return {'type': 'ir.actions.act_window_close'}
