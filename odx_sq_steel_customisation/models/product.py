# -*- coding: utf-8 -*-

from odoo import models, fields, api


class ProductTemplate(models.Model):
    _inherit = 'product.template'

    width_in = fields.Float(string='Width(in)',digits=[6, 4])
    width_mm = fields.Float(string='Width(mm)',digits=[6, 4])
    thk_in = fields.Float(string='Thickness(in)',digits=[6, 4])
    thk_mm = fields.Float(string='Thickness(mm)',digits=[6, 4])
    cut_l_in = fields.Float(string='Cut L(in)',digits=[6, 4])
    cut_l_mm = fields.Float(string='Cut L(mm)',digits=[6, 4])
    length_in = fields.Float(string='Length(in)',digits=[6, 4])
    length_mm = fields.Float(string='Length(mm)',digits=[6, 4])
    weight_lb = fields.Float(string='Weight(lb)',digits=[6, 4])
    weight_mm = fields.Float(string='Weight(kg)',digits=[6, 4])
    od_in = fields.Float(string='OD(in)',digits=[6, 4])
    od_mm = fields.Float(string='OD(mm)',digits=[6, 4])
    product_classificaton = fields.Selection([('plate', 'Plate'), ('rod', 'Rod'), ('sheet', 'Sheet'), ('bar', 'Rectangular Bar')], string='Product Classification', default='plate')


    @api.onchange('categ_id','product_classificaton')
    def _onchange_name(self):
        for record in self:
            record.name = record.categ_id.name +' '+ record.product_classificaton.capitalize()

    @api.onchange('categ_id','product_classificaton')
    def _onchange_classification(self):
        if self.product_classificaton == 'rod':
            self.width_in=0
            self.thk_in=0
            self.cut_l_in=0
        else:
            self.length_in=0
            self.weight_lb=0
            self.od_in=0
    @api.onchange('width_in')
    def _onchange_width(self):
        self.width_mm = self.width_in * 25.4

    @api.onchange('thk_in')
    def _onchange_thickness(self):
        self.thk_mm = self.thk_in * 25.4

    @api.onchange('cut_l_in')
    def _onchange_cut_l(self):
        self.cut_l_mm = self.cut_l_in * 25.4     

    @api.onchange('length_in')
    def _onchange_length(self):
        self.length_mm = self.length_in * 25.4     

    @api.onchange('weight_lb')
    def _onchange_weight(self):
        self.weight_mm = self.weight_lb * 0.45359237

    @api.onchange('od_in')
    def _onchange_od(self):
        self.od_mm = self.od_in * 25.4 

   
#     def name_get(self):
#         result = []
#         for record in self:
#             name = '['+record.default_code+']' + ' ' + record.name + ' ' + record.categ_id.name
#             result.append((record.id, name))
#         return result

# class ProductProduct(models.Model):
#     _inherit = 'product.product'

#     def name_get(self):
#         result = []
#         for record in self:
#             name = '['+record.default_code+']' + ' ' + record.name + ' ' + record.categ_id.name
#             result.append((record.id, name))
#         return result