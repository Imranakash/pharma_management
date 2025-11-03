from odoo import api, fields, models
from io import BytesIO
import base64
import xlsxwriter

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


    # Excel Report
    def action_export_doctor_xlsx(self):
        """Generate and download Excel report for selected doctors"""
        output = BytesIO()
        workbook = xlsxwriter.Workbook(output, {'in_memory': True})
        sheet = workbook.add_worksheet('Doctors')

        # Header format
        header_format = workbook.add_format({'bold': True, 'bg_color': '#D9D9D9'})
        headers = ['Name', 'Specialization', 'Phone', 'Email', 'City', 'Prescription Count']
        for col, header in enumerate(headers):
            sheet.write(0, col, header, header_format)

        # Data rows
        row = 1
        for doctor in self:
            sheet.write(row, 0, doctor.name or '')
            sheet.write(row, 1, doctor.specialization or '')
            sheet.write(row, 2, doctor.phone or '')
            sheet.write(row, 3, doctor.email or '')
            sheet.write(row, 4, doctor.city or '')
            sheet.write(row, 5, doctor.prescription_count or 0)
            row += 1

        workbook.close()
        output.seek(0)
        xlsx_data = output.read()

        attachment = self.env['ir.attachment'].create({
            'name': 'Doctor_Report.xlsx',
            'type': 'binary',
            'datas': base64.b64encode(xlsx_data),
            'res_model': 'pharma.doctor',
            'res_id': self.id,
            'mimetype': 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet',
        })

        # Return download link
        return {
            'type': 'ir.actions.act_url',
            'url': f'/web/content/{attachment.id}?download=true',
            'target': 'new',
        }
