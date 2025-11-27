# -*- coding: utf-8 -*-
from odoo import models, fields, api

class LoadingPlan(models.Model):
    _name = 'loading.plan'
    _description = 'Loading Plan'
    _inherit = ['mail.thread', 'mail.activity.mixin']

    name = fields.Char(string='Reference', required=True, copy=False, readonly=True, default='New')
    purchase_order_id = fields.Many2one('purchase.order', string='Purchase Order', required=True, ondelete='cascade')
    partner_id = fields.Many2one('res.partner', string='Supplier', related='purchase_order_id.partner_id', store=True)
    supplier_type = fields.Selection(related='partner_id.fuel_supplier_type', string='Supplier Type', store=True)
    state = fields.Selection([
        ('draft', 'Draft'),
        ('confirmed', 'Confirmed'),
        ('done', 'Done'),
        ('cancel', 'Cancelled')
    ], string='Status', default='draft', tracking=True)
    
    # ============================================
    # COMMON FIELDS (Used across multiple suppliers)
    # ============================================
    
    # Transport Information (Common)
    transporter_id = fields.Many2one('res.partner', string='Transport Company / Transporter', tracking=True)
    transporter_vehicle_id = fields.Many2one('fleet.vehicle', string='Horse / Truck Registration', domain="[('transporter_id', '=', transporter_id)]", tracking=True)
    trailer_1_id = fields.Many2one('fleet.trailer', string='Trailer Registration', tracking=True)
    trailer_2_id = fields.Many2one('fleet.trailer', string='Trailer Registration 2', tracking=True)
    trailer_3_id = fields.Many2one('fleet.trailer', string='Trailer Registration 3', tracking=True)
    driver_id = fields.Many2one('res.partner', string='Driver Name')
    passport_no = fields.Char(string='Passport / ID No.')
    
    # Order Information (Common)
    po_number = fields.Char(string='PO Number')
    supplier_ref = fields.Char(string='Supplier Reference')
    company_id= fields.Many2one('res.company', string='Company / Customer', ondelete='cascade', default=lambda self: self.env.user.company_id)
    contact_person = fields.Many2one('res.partner', string='Contact Person')
    loading_date_time = fields.Datetime(string='Loading Date & Time', default=fields.Datetime.now)
    
    # Product Information (Common)
    product_id = fields.Many2one('product.product', string='Product')
    product_ulp_qty = fields.Float(string='ULP Quantity')
    product_d50_qty = fields.Float(string='D50 Quantity')
    order_quantity = fields.Float(string='Total Order Quantity')
    destination = fields.Char(string='Destination')
    currency_id = fields.Many2one('res.currency', string='Currency')

    # Compartments (Common across all templates)
    compartment_1 = fields.Float(string='Compartment 1')
    compartment_2 = fields.Float(string='Compartment 2')
    compartment_3 = fields.Float(string='Compartment 3')
    compartment_4 = fields.Float(string='Compartment 4')
    compartment_5 = fields.Float(string='Compartment 5')
    compartment_6 = fields.Float(string='Compartment 6')
    compartment_7 = fields.Float(string='Compartment 7')
    compartment_8 = fields.Float(string='Compartment 8')
    compartment_9 = fields.Float(string='Compartment 9')
    total_compartments = fields.Float(string='Total Capacity', compute='_compute_total_compartments', store=True)

    # ============================================
    # NAMCOR SPECIFIC FIELDS
    # ============================================
    namcor_loading_time = fields.Float(string='Loading Time (Namcor)')
    namcor_loaded = fields.Selection([('yes', 'Yes'), ('no', 'No')], string='Loaded (Y/N)')
    
    # ============================================
    # PUMA ENERGY SPECIFIC FIELDS
    # ============================================
    puma_epuma_order_no = fields.Char(string='ePuma Order No.')
    puma_epuma_load_code = fields.Char(string='ePuma Load Code')
    puma_product_50ppm = fields.Char(string='Product 50PPM Diesel')
    puma_order_volumes = fields.Char(string='Order Volumes')
    puma_status = fields.Char(string='Status (Impala dispatch only)')

    # ============================================
    # VIVO SPECIFIC FIELDS
    # ============================================
    vivo_customer_sold_acc = fields.Char(string='Customer Sold to Account')
    vivo_customer_ship_acc = fields.Char(string='Customer Ship to Account')
    vivo_cpl_order_no = fields.Char(string='CPL Customer Order Number')
    unit_price = fields.Monetary(string=' Cost per Lt', currency_field="currency_id")
    total_cost = fields.Monetary(string='Total Cost', currency_field="currency_id")


    # ============================================
    # SASOL SPECIFIC FIELDS
    # ============================================
    sasol_sold_to_party = fields.Char(string='Sold-to Party')
    sasol_ship_to_party = fields.Char(string='Ship-to Party')
    sasol_consignee = fields.Char(string='Consignee')
    sasol_carrier_code = fields.Char(string='Carrier Code')
    border_post = fields.Char(string='Border Post')
    sasol_plant = fields.Char(string='Plant')
    sasol_contact_number = fields.Char(string='Contract Number')
    sasol_mode_transport = fields.Char(string='Mode of transport')
    sasol_quantity_l20 = fields.Float(string='Quantity in L20', compute='_compute_sasol_quantity_l20')
    sasol_sales_unit = fields.Char(string='Sales Unit', default='M3')

    
    # ============================================
    # COMPUTED FIELDS
    # ============================================
    
    @api.depends('compartment_1', 'compartment_2', 'compartment_3', 'compartment_4', 
                 'compartment_5', 'compartment_6', 'compartment_7', 'compartment_8', 'compartment_9')
    def _compute_total_compartments(self):
        for record in self:
            record.total_compartments = sum([
                record.compartment_1 or 0,
                record.compartment_2 or 0,
                record.compartment_3 or 0,
                record.compartment_4 or 0,
                record.compartment_5 or 0,
                record.compartment_6 or 0,
                record.compartment_7 or 0,
                record.compartment_8 or 0,
                record.compartment_9 or 0,
            ])

    @api.depends('product_d50_qty', 'product_ulp_qty')
    def _compute_sasol_quantity_l20(self):
        for record in self:
            if record.product_d50_qty:
                record.sasol_quantity_l20 = record.product_d50_qty/1000
            if record.product_ulp_qty:
                record.sasol_quantity_l20 = record

    
    @api.model_create_multi
    def create(self, vals):
        for val in vals:
            if val.get('name', 'New') == 'New':
                val['name'] = self.env['ir.sequence'].next_by_code('loading.plan') or 'New'
        return super(LoadingPlan, self).create(vals)

    @api.onchange('transporter_id')
    def _onchange_transporter_id(self):
        if not self.transporter_id:
            self.transporter_vehicle_id = False
            self.driver_id = False
            self.trailer_1_id = False
            self.trailer_2_id = False
            self.trailer_3_id = False
        else:
            if self.transporter_vehicle_id and self.transporter_vehicle_id.transporter_id != self.transporter_id:
                self.transporter_vehicle_id = False

    @api.onchange('transporter_vehicle_id')
    def _onchange_transporter_vehicle_id(self):
        if self.transporter_vehicle_id:
            self.trailer_1_id = self.transporter_vehicle_id.trailer_1_id
            self.trailer_2_id = self.transporter_vehicle_id.trailer_2_id
            self.trailer_3_id = self.transporter_vehicle_id.trailer_3_id
            self.driver_id = self.transporter_vehicle_id.driver_id

        else:
            self.trailer_1_id = False
            self.trailer_2_id = False
            self.trailer_3_id = False
            self.driver_id = False

    @api.model
    def default_get(self, fields_list):
        res = super(LoadingPlan, self).default_get(fields_list)
        if 'purchase_order_id' in res:
            po = self.env['purchase.order'].browse(res['purchase_order_id'])
            if po:
                res.update({
                    'transporter_id': po.transporter_id.id,
                    'transporter_vehicle_id': po.transporter_vehicle_id.id,
                    'driver_id': po.transporter_vehicle_id.driver_id.id,
                    'trailer_1_id': po.trailer_1_id.id,
                    'trailer_2_id': po.trailer_2_id.id,
                    'trailer_3_id': po.trailer_3_id.id,
                })
        return res

    @api.onchange('purchase_order_id')
    def _onchange_purchase_order_id(self):
        if self.purchase_order_id:
            self.transporter_id = self.purchase_order_id.transporter_id
            self.transporter_vehicle_id = self.purchase_order_id.transporter_vehicle_id
            self.trailer_1_id = self.purchase_order_id.trailer_1_id
            self.trailer_2_id = self.purchase_order_id.trailer_2_id
            self.trailer_3_id = self.purchase_order_id.trailer_3_id
            self.driver_id = self.purchase_order_id.transporter_vehicle_id.driver_id

            product_ulp_qty = 0.0
            product_d50_qty = 0.0
            order_quantity = 0.0
            
            for line in self.purchase_order_id.order_line:
                if line.product_id.product_identifier == 'petrol':
                    product_ulp_qty += line.product_qty
                    order_quantity += line.product_qty
                elif line.product_id.product_identifier == 'diesel':
                    product_d50_qty += line.product_qty
                    order_quantity += line.product_qty

                self.unit_price = line.price_unit
                self.product_id = line.product_id
            
            self.product_ulp_qty = product_ulp_qty
            self.product_d50_qty = product_d50_qty
            self.order_quantity = order_quantity


    def action_confirm(self):
        self.write({'state': 'confirmed'})
    
    def action_done(self):
        self.write({'state': 'done'})
    
    def action_cancel(self):
        self.write({'state': 'cancel'})
    
    def action_draft(self):
        self.write({'state': 'draft'})
    
    def action_print_loading_plan(self):
        return self.env.ref('vkd_loading_plan.action_report_loading_plan').report_action(self)
