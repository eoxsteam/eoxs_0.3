from odoo import models, fields, api, _


class StockProductionLot(models.Model):
    _inherit = 'stock.production.lot'

    @api.model
    def create(self, vals):
        if vals.get('name', _('New')) == _('New'):
            if not self.env.context.get('baby_lot'):
                vals['name'] = self.env['ir.sequence'].next_by_code('stock.lot.serial.custom') or _('New')
            else:
                vals['name'] = self.env['ir.sequence'].next_by_code('stock.lot.serial.baby.coil') or _('New')
        return super(StockProductionLot, self).create(vals)

    @api.onchange('vendor_id')
    def _get_vendor_list(self):
        if self.vendor_id:
            partners = self.env['res.partner'].search([('parent_id', '=', self.vendor_id.id)])
            model_fields_domain = [('id', 'in', partners.ids)]
            return {'domain': {'vendor_location_id': model_fields_domain, }}

    # @api.onchange('category_id')
    # def _get_category_list(self):
    #     if self.category_id:
    #         fields_domain = [('parent_id', '=', self.category_id.id)]
    #         return {'domain': {'sub_category_id': fields_domain, }}
    #     else:
    #         return {'domain': {'sub_category_id': []}}

    @api.onchange('category_id')
    def _domain_product_id(self):
        if self.category_id:
            return {'domain': {'product_id': [('categ_id', '=', self.category_id.id)]}}
        else:
            return {'domain': {'product_id': []}}
        
    @api.onchange('vendor_id')
    def _onchange_vendor_serial(self):
        if self.vendor_id.vendor_serial_number:
            self.vendor_serial_number = self.vendor_id.vendor_serial_number

    def _compute_image_512(self):
        """Get the image from the template if no image is set on the variant."""
        for record in self:
            record.image_512 = record.image

    def _compute_image_256(self):
        """Get the image from the template if no image is set on the variant."""
        for record in self:
            record.image_256 = record.image_variant_256 or record.product_tmpl_id.image_256

    def _compute_image_128(self):
        """Get the image from the template if no image is set on the variant."""
        for record in self:
            record.image_128 = record.image_variant_128 or record.product_tmpl_id.image_128

    name = fields.Char(
        'Lot Number', required=True, help="Unique Lot/Serial Number")
    # default = lambda self: self.env['ir.sequence'].next_by_code('stock.lot.serial.custom')

    image_1920 = fields.Image("Coil Image", max_width=1920, max_height=1920)

    image_512 = fields.Image("Image 512", related="image_1920", max_width=512, max_height=512,
                             store=True)
    image_256 = fields.Image("Image 256", related="image_1920", max_width=256, max_height=256,
                             store=True)
    image_128 = fields.Image("Image 128", related="image_1920", max_width=128, max_height=128,
                             store=True)

    surface_finish_id = fields.Many2one("surface.finish", string="Surface Finish Type", track_visibility="onchange", )
    vendor_serial_number = fields.Char(string="Vendor Serial Number", track_visibility="onchange")
    # purchase
    heat_number = fields.Char(string='Heat Number')
    lift_number = fields.Char(string='Lift Number')
    part_number = fields.Char(string='Part Number')
    tag_number = fields.Char(string='Tag Number')

    heat_number_pr1 = fields.Char(string='Heat Number')
    lift_number_pr1 = fields.Char(string='Lift Number')
    part_number_pr1 = fields.Char(string='Part Number')
    tag_number_pr1 = fields.Char(string='Tag Number')
    job_order_lot = fields.Boolean(string='Job order Lot', default=False)

    # picking
    sale_order_id = fields.Many2one('sale.order', string="Sale Reference", track_visibility="onchange")
    # sale_ref_ids = fields.Many2many('sale.order', string="Sale Reference", compute="_compute_sale_ref",
    #                                 track_visibility="onchange")

    vendor_name = fields.Char(string="Vendor Name", related="vendor_id.name", track_visibility="onchange")
    vendor_id = fields.Many2one('res.partner', string="Vendor", track_visibility="onchange")
    bill_of_lading = fields.Char(string="Bill of Lading", track_visibility="onchange")
    vendor_location_id = fields.Many2one('res.partner', string="Vendor Location", track_visibility="onchange",
                                         domain=lambda self: self._get_vendor_list())
    vendor = fields.Text(string="Vendor Note", track_visibility="onchange")
    category = fields.Text(string="Category", track_visibility="onchange")
    internal = fields.Text(string="Internal", track_visibility="onchange")

    date_removed = fields.Date(string="Date Removed", track_visibility="onchange")
    packing_slip_no = fields.Char(string="Packing Slip No.", track_visibility="onchange")
    internet_serial = fields.Char(string="R#", track_visibility="onchange")
    date_received = fields.Date(string="Date Received", track_visibility="onchange")
    po_number = fields.Char(string="PO Number", track_visibility="onchange")
    loc_city = fields.Many2one('stock.location', string="Location-City",
                               track_visibility="onchange")
    loc_warehouse = fields.Many2one('stock.warehouse', string="Location-Warehouse", track_visibility="onchange")
    stock_status = fields.Selection([
        ('transit', 'In Transit'),
        ('available', 'Available'),
        ('reserved', 'Reserved'),
        ('in_production', 'In production'),
        ('not_available', 'Not available')
    ], string='Stock Status', default='available', track_visibility="onchange")
    material_type = fields.Selection([
        ('coil', 'Coil'),
        ('sheets', 'Sheets'),
    ], default='coil', string='Material Type', track_visibility="onchange")
    number_of_sheets = fields.Integer(string="Number Of Sheets")
    is_child_coil = fields.Boolean(string="Is Child Coil")
    parent_coil_id = fields.Many2one('stock.production.lot', string="Parent Coil")

    category_id = fields.Many2one('product.category', string="Product Type", 
        # domain="[('parent_id', '=', False)]",
                                  track_visibility="onchange", )
    # sub_category_id = fields.Many2one('product.category', string="Sub Category", track_visibility="onchange",
    #                                   domain="[('parent_id', '=', category_id) or [] ] ")
    # domain=lambda self: self._get_category_list())
    product_classificaton = fields.Selection([('plate', 'Plate'), ('rod', 'Rod'), ('sheet', 'Sheet'), ('bar', 'Rectangular Bar')], string='Product Classification', default='plate')

    product_template_id = fields.Many2one('product.template', string="Product Template", track_visibility="onchange")
    product_id = fields.Many2one('product.product', 'Product', domain=lambda self: self._domain_product_id(),
                                 required=True, check_company=True, track_visibility="onchange")
    quality = fields.Char(string='Quality', track_visibility="onchange")
    location = fields.Char(string='Location', track_visibility="onchange")

    # width_in = fields.Float(string='Width(in)', track_visibility="onchange", digits=[6, 4])
    # width_mm = fields.Float(string='Width(mm)', track_visibility="onchange", digits=[8, 2])
    # thickness_in = fields.Float(string='Thickness(in)', track_visibility="onchange", digits=[6, 4])
    # thickness_mm = fields.Float(string='Thickness(mm)', track_visibility="onchange", digits=[8, 2])
    thickness_spec = fields.Char(string='Thickness Spec', track_visibility="onchange")
    # length_in = fields.Float(string='Length(in)', track_visibility="onchange", digits=[8, 4])
    # length_mm = fields.Float(string='Length(mm)', track_visibility="onchange", digits=[8, 2])

    width_in = fields.Float(string='Width(in)',digits=[6, 4])
    width_mm = fields.Float(string='Width(mm)',digits=[6, 4])
    thk_in = fields.Float(string='Thickness(in)',digits=[6, 4])
    thk_mm = fields.Float(string='Thickness(mm)',digits=[6, 4])
    cut_l_in = fields.Float(string='Cut L(in)',digits=[6, 4])
    cut_l_mm = fields.Float(string='Cut L(mm)',digits=[6, 4])
    length_in = fields.Float(string='Length(in)',digits=[6, 4])
    length_mm = fields.Float(string='Length(mm)',digits=[6, 4])
    weight_lb = fields.Float(string='Weight(lb)',digits=[6, 4])
    weight_mm = fields.Float(string='Weight(mm)',digits=[6, 4])
    od_in = fields.Float(string='OD(in)',digits=[6, 4])
    od_mm = fields.Float(string='OD(mm)',digits=[6, 4])

    # product_qty = fields.Float(string=' ', track_visibility="onchange", digits=(5, 2), )
    # related='product_qty'
    weight_kg = fields.Float(string='Weight(Kg)', track_visibility="onchange", compute='_compute_weight_kg')
    piw = fields.Integer(string='PIW', compute='_compute_piw', redaonly=1)

    grade = fields.Char(string='Grade', track_visibility="onchange")

    rockwell = fields.Float(string='Rock_well', track_visibility="onchange", digits=(5, 1))
    yield_mpa = fields.Float(string='Yield(mpa)', track_visibility="onchange")
    yield_psi = fields.Float(string='Yield(psi)', track_visibility="onchange")
    yield_ksi = fields.Float(string='Yield(ksi)', track_visibility="onchange")
    tensile_mpa = fields.Float(string='Tensile(mpa)', track_visibility="onchange")
    tensile_psi = fields.Float(string='Tensile(psi)', track_visibility="onchange")
    tensile_ksi = fields.Float(string='Tensile(ksi)', track_visibility="onchange")
    elongation = fields.Float(string='Elongation', track_visibility="onchange")
    # component_ids = fields.One2many('product.components', 'stock_component_id', default=_default_product_components)

    pass_oil = fields.Char(string="Pass/Oil")
    finish = fields.Char(string="Finish")
    temper = fields.Char(string="Temper")
    coating = fields.Char(string="Coating")
    # mill = fields.Char(string="Mill")
    # mill_sr_no = fields.Char(string="Mill SR No.")

    comp_c = fields.Float(string="C", digits=[4, 3])
    comp_mn = fields.Float(string="MN", digits=[4, 3])
    comp_p = fields.Float(string="P", digits=[4, 3])
    comp_s = fields.Float(string="S", digits=[4, 3])
    comp_si = fields.Float(string="SI", digits=[4, 3])
    comp_al = fields.Float(string="AL", digits=[4, 3])
    comp_cr = fields.Float(string="CR", digits=[4, 3])
    comp_nb = fields.Float(string="NB", digits=[4, 3])
    comp_ti = fields.Float(string="TI", digits=[4, 3])
    comp_ca = fields.Float(string="CA", digits=[4, 3])
    comp_n = fields.Float(string="N", digits=[4, 3])
    comp_ni = fields.Float(string="NI", digits=[4, 3])
    comp_cu = fields.Float(string="CU", digits=[4, 3])
    comp_v = fields.Float(string="V", digits=[4, 3])
    comp_b = fields.Float(string="B", digits=[4, 3])

    comp_co = fields.Float(string="Cb", digits=[4, 3])
    comp_mo = fields.Float(string="Mo", digits=[4, 3])
    comp_sn = fields.Float(string="Sn", digits=[4, 3])

    state = fields.Selection([('draft', 'Draft'), ('confirm', 'Confirm')],
                             default='draft', track_visibility="onchange")

    purchase_cost = fields.Float(string="Unit Purchase Cost")
    landed_cost = fields.Float(string="Unit Landed Cost")
    total_purcahse_cost = fields.Float(string="Total Purcahse Cost")
    total_landed_cost = fields.Float(string="Total Landed Cost")

    def action_view_lot_history(self):

        parent_lot_list = []
        child_lots = []
        parent_coil = self.parent_coil_id.name if self.parent_coil_id else ""
        similar_options = []
        table = ''
        table += '''
                    <table class="table table-bordered" style="text-align: center; width:100%;">
                <thead>
                    <tr>
                        <td><b><font style="color: #2196F3;">Source</font></b><br></td>
                        <td><b><font style="color: #2196F3;">Lot Number</font></b><br></td>
                        <td><b><font style="color: #2196F3;">Child Lots</font></b><br></td>           
                    </tr>
                    <tr>
                        <td><b><font style="color: #000000;">''' + str(
            parent_coil) + '''</font></b><br></td>
                        <td><b><font style="color: #000000;">''' + str(
            self.name) + '''</font></b><br></td>
                       <td><b><font style="color: #000000;">''' + str(
        ) + '''</font></b><br></td>
                               
                    </tr>
                </thead>
                <tbody>
                 '''

        child_lots = self.search([('parent_coil_id.id', '=', self.id)])

        if child_lots:
            for line in child_lots:
                table += '''
                    <tr>
                        <td><b><font style="color: #000000;">''' + str(
                ) + '''</font></b><br></td>
                        <td><b><font style="color: #000000;">''' + str(
                ) + '''</font></b><br></td>
                        <td><b><font style="color: #000000;">''' + str(
                    line.name) + '''</font></b> ''' + str(line.material_type) + '''<br></td>
                    </tr>
                        '''
        table += ''' </tbody>
                      </table>
                       '''

        # if similar_options:
        return {
            'name': _('Lot History'),
            'type': 'ir.actions.act_window',
            'view_mode': 'form',
            'res_model': 'display.options.wizard',
            'views': [(False, 'form')],
            'view_id': False,
            'target': 'new',
            'context': {
                'default_memo': table,
                'default_lot_ref_id': self.id}
        }

    def get_serial_barcode(self):
        return self.env.ref('odx_product_custom_steel.action_serial_barcode_generator_lot').report_action(self)

    def set_to_draft(self):
        if self.state == 'confirm':
            self.write({'state': 'draft'})

    def set_to_confirm(self):
        if self.state == 'draft':
            self.write({'state': 'confirm'})

    @api.onchange('product_id')
    def onchange_product_id(self):
        if self.product_id:
            self.product_classificaton = self.product_id.product_classificaton


    # @api.onchange('width_in')
    # def _onchange_width(self):
    #     self.width_mm = self.width_in * 25.4

    # @api.onchange('thickness_in')
    # def _onchange_thickness(self):
    #     self.thickness_mm = self.thickness_in * 25.4

    # @api.onchange('length_in')
    # def _onchange_length(self):
    #     self.length_mm = self.length_in * 25.4
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
        self.weight_mm = self.weight_lb * 25.4 

    @api.onchange('od_in')
    def _onchange_od(self):
        self.od_mm = self.od_in * 25.4 

    @api.depends('product_qty')
    def _compute_weight_kg(self):
        self.weight_kg = False
        for rec in self:
            rec.weight_kg = rec.product_qty * 0.45359237

    def _compute_piw(self):
        self.piw = False
        for rec in self:
            if rec.product_qty > 0 and rec.width_in > 0:
                rec.piw = rec.product_qty / rec.width_in

    def _compute_sale_ref(self):
        self.sale_ref_ids = False
        sale_line_id_list = []
        for rec in self:
            sale_line = self.env['sale.order.line'].search([('lot_id', '=', self.id)])
            # sale_line = self.env['sale.order.line'].search([])
            production_line = self.env['sale.order.line'].search([]).mapped('production_lot_ids')
            production = self.env['sale.order.line'].search([]).mapped('production_lot_ids').mapped(
                'production_line_ids')
            for line in sale_line:
                if line.lot_id.id == self.id:
                    sale_line_id_list.append(line.order_id.id)
                    self.write({'sale_ref_ids': [(4, line.order_id.id)]})
            for record in production_line:
                if record.lot_id.id == self.id:
                    if record.state != 'cancel':
                        sale_line_id_list.append(record.sale_line_id.order_id.id)
                        self.write({'sale_ref_ids': [(4, record.sale_line_id.order_id.id)]})

            for pl in production:
                if pl.finished_lot_id.id == self.id:
                    if pl.is_balance == False:
                        self.write({'sale_ref_ids': [(4, pl.production_ref_id.sale_order_id.id)]})