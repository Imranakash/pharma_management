from odoo import models

class DoctorReport(models.AbstractModel):
    _name = 'report.pharma.doctor_report_template'
    _description = 'Doctor Report'

    def _get_report_values(self, docids, data=None):
        docs = self.env['pharma.doctor'].browse(docids)
        result = []
        for doc in docs:
            prescriptions = self.env['pharma.prescription'].search([('doctor_id', '=', doc.id)])
            total_value = sum(p.total_amount for p in prescriptions)
            result.append({
                'doctor': doc,
                'prescriptions': prescriptions,
                'total_value': total_value,
            })
        return {
            'docs': result,
        }
