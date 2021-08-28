from odoo import api, fields, models, _
from odoo.exceptions import ValidationError


class ProductQuotation(models.Model):
    _name = "product.quotation"

    def line_duplicate(self):
        for line in self:
            line.copy()

    @api.onchange('product_category_id')
    def _get_category_list(self):
        self.product_id = False
        if self.product_category_id:
            fields_domain = [('parent_id', '=', self.product_category_id.id)]
            return {'domain': {'sub_category_id': fields_domain, }}
        else:
            return {'domain': {'sub_category_id': []}}

    @api.onchange('category_id', 'sub_category_id')
    def _domain_product_id(self):
        if self.sub_category_id:
            return {'domain': {'product_id': [('categ_id', '=', self.sub_category_id.id)]}}
        else:
            return {'domain': {'product_id': []}}

    @api.onchange('product_id')
    def _onchange_product_id(self):
        if self.product_id:
            self.uom_id = self.product_id.uom_id.id

    product_category_id = fields.Many2one('product.category', 'Category', domain="[('parent_id', '=', False)]")
    sub_category_id = fields.Many2one('product.category', string="Sub Category", track_visibility="onchange",
                                      domain="[('parent_id', '=', product_category_id) or [] ] ")
    product_id = fields.Many2one('product.product', string='Sub Product')
    descriptions = fields.Text(string='Description',required=True)
    product_qty = fields.Float(string='Weight')
    uom_id = fields.Many2one('uom.uom', string='UOM')
    vrm_reference_id = fields.Many2one('vrm.lead', string='Vrm')
