{
    'name': 'Pharma Management System',
    'version': '1.0',
    'category': 'Healthcare',
    'summary': 'Manage doctors, medical representatives, prescriptions, visits, and medicine sales',
    'description': """
PharmaTrack Pvt. Ltd. - Pharma Management System
================================================
A comprehensive pharmaceutical management solution for PharmaTrack Pvt. Ltd.

Key Features:
--------------
- Manage doctors and their specialties
- Manage medical representatives (MRs)
- Manage medicines and prescriptions
- Track MR visits and doctor interactions
- Record prescription details and distributed samples
- Sales and performance reporting
    """,
    'author': 'PharmaTrack Pvt. Ltd.',
    'website': 'https://www.pharmatrack.com',
    'depends': ['base', 'hr', 'sale', 'stock', 'mail'],
    'data': [
        # 'security/pharma_group.xml',
        'security/ir.model.access.csv',
        # 'data/record_rules.xml',
        'wizard/prescription.xml',
        'views/pharma_doctor.xml',
        'views/pharma_representative.xml',
        'views/pharma_medicine.xml',
        'views/pharma_prescription.xml',
        'report/pharma_doctor_template.xml',
        'report/pharma_doctor_action.xml',
        'views/menu.xml',
    ],
    'application': True,
    'installable': True,
    'auto_install': False,
    'license': 'LGPL-3',
}
