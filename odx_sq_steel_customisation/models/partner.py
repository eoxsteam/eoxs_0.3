from odoo import models, fields, api


class ResPartner(models.Model):
    _inherit = 'res.partner'

    vendor_serial_number = fields.Char(string='Vendor Serial Number')
