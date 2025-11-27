import base64
import io
from odoo import models, fields, _
from odoo.exceptions import UserError
from odoo.tools.misc import xlsxwriter


class LoadingPlanReport(models.TransientModel):
    _name = 'loading.plan.report'
    _description = 'Loading Plan  Export'

    date_from = fields.Date(string='Start Date', required=True, default=fields.Date.context_today)
    date_to = fields.Date(string='End Date', required=True, default=fields.Date.context_today)
    supplier_type = fields.Selection([
        ('namcor', 'Namcor'),
        ('puma', 'Puma'),
        ('vivo', 'Vivo'),
        ('sasol', 'Sasol'),
        ('standard', 'Standard'),
    ], string='Fuel Supplier Type', required=True)

    def action_generate_report(self):
        output = io.BytesIO()
        workbook = xlsxwriter.Workbook(output, {'in_memory': True})

        domain = [
            ('supplier_type', '=', self.supplier_type),
            ('loading_date_time', '>=', self.date_from),
            ('loading_date_time', '<=', self.date_to)
        ]
        plans = self.env['loading.plan'].search(domain, order='loading_date_time asc')

        if self.supplier_type == 'sasol':
            self._generate_sasol_report(workbook, plans)
        elif self.supplier_type == 'namcor':
            self._generate_namcor_report(workbook, plans)
        elif self.supplier_type == 'vivo':
            self._generate_vivo_report(workbook, plans)
        elif self.supplier_type == 'puma':
            self._generate_puma_report(workbook, plans)
        else:
            self._generate_standard_report(workbook, plans)

        workbook.close()
        output.seek(0)
        encoded_data = base64.b64encode(output.getvalue()).decode('utf-8')
        output.close()

        filename = f"{self.supplier_type.upper()}_Loading_Plan_{self.date_from}_{self.date_to}.xlsx"
        attachment = self.env['ir.attachment'].create({
            'name': filename,
            'datas': encoded_data,
            'res_model': self._name,
            'type': 'binary',
            'mimetype': 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet',
        })

        return {
            "type": "ir.actions.act_url",
            "url": f"/web/content/{attachment.id}?download=true",
            "target": "self",
        }

    def _get_formats(self, workbook):
        return {
            'header': workbook.add_format(
                {'bold': True, 'border': 1, 'bg_color': '#D3D3D3', 'align': 'center', 'valign': 'vcenter'}),
            'date': workbook.add_format({'num_format': 'dd/mm/yyyy', 'border': 1}),
            'cell': workbook.add_format({'border': 1}),
            'number': workbook.add_format({'border': 1, 'num_format': '#,##0.00'}),
            'sasol_green': workbook.add_format({'bold': True, 'border': 1, 'bg_color': '#92D050', 'align': 'center'}),
            'vivo_blue': workbook.add_format({'bold': True, 'border': 1, 'bg_color': '#BDD7EE', 'align': 'center'}),
        }

    def _generate_sasol_report(self, workbook, plans):
        sheet = workbook.add_worksheet('Sasol Upload')
        fmt = self._get_formats(workbook)

        headers = [
            'Sold-to party', 'Ship-to party', 'Consignee', 'BORDER POST',
            'Carrier code', 'Plant', 'Material', 'Quantity in L20',
            'Sales unit', 'Mode of transport', 'Contract Number', 'PO number'
        ]

        for col, head in enumerate(headers):
            style = fmt['sasol_green']
            sheet.write(0, col, head, style)
            sheet.set_column(col, col, 15)

        row = 1
        for p in plans:
            sheet.write(row, 0, p.sasol_sold_to_party or '', fmt['cell'])
            sheet.write(row, 1, p.sasol_ship_to_party or '', fmt['cell'])
            sheet.write(row, 2, p.sasol_consignee or '', fmt['cell'])
            sheet.write(row, 3, p.border_post or '', fmt['cell'])
            sheet.write(row, 4, p.sasol_carrier_code or '', fmt['cell'])
            sheet.write(row, 5, p.sasol_plant or '', fmt['cell'])
            sheet.write(row, 6, p.product_id.name or '', fmt['cell'])
            sheet.write(row, 7, p.sasol_quantity_l20 or 0.0, fmt['number'])
            sheet.write(row, 8, p.sasol_sales_unit or 'M3', fmt['cell'])
            sheet.write(row, 9, p.sasol_mode_transport or '', fmt['cell'])
            sheet.write(row, 10, p.sasol_contact_number or '', fmt['cell'])
            sheet.write(row, 11, p.po_number or '', fmt['cell'])
            row += 1

    def _generate_namcor_report(self, workbook, plans):
        sheet = workbook.add_worksheet('Namcor Plan')
        fmt = self._get_formats(workbook)

        headers = [
            'Transporter Company', 'Horse registration', 'Trailer Registration', 'Trailer Registration 2', 'Trailer Registration 3', 'Driver name', 'Passport No.',
            'PO #', 'Supplier Ref', 'Contact person', 'Company', 'Loading Date', 'Loading Time' , 'Product ULP Quantity', 'Product D50 Quantity'
        ]
        headers.extend([f'Comp {i}' for i in range(1, 10)])
        headers.extend(['Loaded'])

        for col, head in enumerate(headers):
            sheet.write(0, col, head, fmt['header'])
            sheet.set_column(col, col, 15)

        row = 1
        for p in plans:
            sheet.write(row, 0, p.transporter_id.name or '', fmt['cell'])
            sheet.write(row, 1, p.transporter_vehicle_id.license_plate or '', fmt['cell'])
            sheet.write(row, 2, p.trailer_1_id.license_plate or '', fmt['cell'])
            sheet.write(row, 3, p.trailer_2_id.license_plate or '', fmt['cell'])
            sheet.write(row, 4, p.trailer_3_id.license_plate or '', fmt['cell'])
            sheet.write(row, 5, p.driver_id.name or '', fmt['cell'])
            sheet.write(row, 6, p.passport_no or '', fmt['cell'])
            sheet.write(row, 7, p.po_number or '', fmt['cell'])
            sheet.write(row, 8, p.supplier_ref or '', fmt['cell'])
            sheet.write(row, 9, p.contact_person.name or '', fmt['cell'])
            sheet.write(row, 10, p.company_id.name or '', fmt['cell'])
            sheet.write(row, 11, p.loading_date_time, fmt['date'])
            sheet.write(row, 12, p.namcor_loading_time or 0.0, fmt['number'])
            sheet.write(row, 13, p.product_ulp_qty or '', fmt['number'])
            sheet.write(row, 14, p.product_d50_qty or '', fmt['number'])

            comps = [p.compartment_1, p.compartment_2, p.compartment_3, p.compartment_4,
                     p.compartment_5, p.compartment_6, p.compartment_7, p.compartment_8, p.compartment_9]
            clm = 0
            for i, val in enumerate(comps):
                sheet.write(row, 15 + i, val or 0, fmt['number'])
                clm = 15+i
            sheet.write(row, clm+1, dict(p._fields['namcor_loaded'].selection).get(p.namcor_loaded) or '', fmt['cell'])
            row += 1

    def _generate_vivo_report(self, workbook, plans):
        sheet = workbook.add_worksheet('Vivo Schedule')
        fmt = self._get_formats(workbook)

        headers = [
            'Customer Sold to Account', 'Customer Ship to Account', 'Delivery Address',
            'Border Post', 'CPL Customer Order Number', 'VIVO ORDER NUMBER',
            'Transporter', 'Driver name', 'Loading Date', 'CUSTOMER NAME',
            'Vehicle Reg Number', 'Tanker Reg Number 1', 'Tanker Reg Number 2', 'Cost per Lt',
            'Total Cost', '50PPM AGO/ need to check', 'TOTAL CAPACITY'
        ]
        headers.extend([f'Comp {i}' for i in range(1, 10)])

        for col, head in enumerate(headers):
            sheet.write(0, col, head, fmt['vivo_blue'])
            sheet.set_column(col, col, 18)

        row = 1
        for p in plans:
            sheet.write(row, 0, p.vivo_customer_sold_acc or '', fmt['cell'])
            sheet.write(row, 1, p.vivo_customer_ship_acc or '', fmt['cell'])
            sheet.write(row, 2, p.destination or '', fmt['cell'])
            sheet.write(row, 3, p.border_post or '', fmt['cell'])
            sheet.write(row, 4, p.vivo_cpl_order_no or '', fmt['cell'])
            sheet.write(row, 5, p.po_number or '', fmt['cell'])
            sheet.write(row, 6, p.transporter_id.name or '', fmt['cell'])
            sheet.write(row, 7, p.driver_id.name or '', fmt['cell'])
            sheet.write(row, 8, p.loading_date_time, fmt['date'])
            sheet.write(row, 9, p.company_id.name or '', fmt['cell'])
            sheet.write(row, 10, p.transporter_vehicle_id.license_plate or '', fmt['cell'])

            # Separate Trailer Columns
            sheet.write(row, 11, p.trailer_1_id.license_plate or '', fmt['cell'])
            sheet.write(row, 12, p.trailer_2_id.license_plate or '', fmt['cell'])

            sheet.write(row, 13, p.unit_price or 0.0, fmt['number'])
            sheet.write(row, 14, p.total_cost or 0.0, fmt['number'])
            sheet.write(row, 15, p.total_cost or 0.0, fmt['number'])
            sheet.write(row, 16, p.total_compartments or 0.0, fmt['number'])

            comps = [p.compartment_1, p.compartment_2, p.compartment_3, p.compartment_4,
                     p.compartment_5, p.compartment_6, p.compartment_7, p.compartment_8, p.compartment_9]
            for i, val in enumerate(comps):
                sheet.write(row, 17 + i, val or 0, fmt['number'])
            row += 1

    def _generate_puma_report(self, workbook, plans):
        sheet = workbook.add_worksheet('Puma NCI')
        fmt = self._get_formats(workbook)

        headers = [
            'Status (Impala)', 'No.', 'Customer(Billing)', 'Contact person',
            'Transport company', 'Horse registration', 'Trailer registration', 'Trailer registration 2',
            'Driver name', 'Destination', 'PO.# & Trade no. ', 'ePuma order no.',
            'ePuma load code', 'Loading date (dd/mmm)', 'Product', 'Order volumes',
        ]
        headers.extend([f'Compart. {i}' for i in range(1, 10)])

        for col, head in enumerate(headers):
            sheet.write(0, col, head, fmt['header'])
            sheet.set_column(col, col, 15)

        row = 1
        count = 1
        for p in plans:
            po_trade = f"{p.po_number or ''}".strip()

            sheet.write(row, 0, p.puma_status or '', fmt['cell'])
            sheet.write(row, 1, count, fmt['cell'])
            sheet.write(row, 2, p.company_id.name or '', fmt['cell'])
            sheet.write(row, 3, p.contact_person.name or '', fmt['cell'])
            sheet.write(row, 4, p.transporter_id.name or '', fmt['cell'])
            sheet.write(row, 5, p.transporter_vehicle_id.license_plate or '', fmt['cell'])

            # Separate Trailer Columns
            sheet.write(row, 6, p.trailer_1_id.license_plate or '', fmt['cell'])
            sheet.write(row, 7, p.trailer_2_id.license_plate or '', fmt['cell'])

            sheet.write(row, 8, p.driver_id.name or '', fmt['cell'])
            sheet.write(row, 9, p.company_id.name or '', fmt['cell'])
            sheet.write(row, 10, po_trade, fmt['cell'])
            sheet.write(row, 11, p.puma_epuma_order_no or '', fmt['cell'])
            sheet.write(row, 12, p.puma_epuma_load_code or '', fmt['cell'])
            sheet.write(row, 13, p.loading_date_time, fmt['date'])
            sheet.write(row, 14, p.product_id.name or '', fmt['cell'])
            sheet.write(row, 15, p.order_quantity or '', fmt['number'])

            comps = [p.compartment_1, p.compartment_2, p.compartment_3, p.compartment_4,
                     p.compartment_5, p.compartment_6, p.compartment_7, p.compartment_8, p.compartment_9]
            for i, val in enumerate(comps):
                sheet.write(row, 16 + i, val or 0, fmt['number'])

            row += 1
            count += 1

    def _generate_standard_report(self, workbook, plans):
        sheet = workbook.add_worksheet('Loading Plan')
        fmt = self._get_formats(workbook)

        headers = ['Date', 'PO Number', 'Transporter', 'Driver', 'Horse', 'Trailer 1', 'Trailer 2', 'Product',
                   'Total Qty']
        headers.extend([f'Comp {i}' for i in range(1, 10)])

        for col, head in enumerate(headers):
            sheet.write(0, col, head, fmt['header'])
            sheet.set_column(col, col, 15)

        row = 1
        for p in plans:
            sheet.write(row, 0, p.loading_date_time, fmt['date'])
            sheet.write(row, 1, p.po_number or '', fmt['cell'])
            sheet.write(row, 2, p.transporter_id.name or '', fmt['cell'])
            sheet.write(row, 3, p.driver_id.name or '', fmt['cell'])
            sheet.write(row, 4, p.transporter_vehicle_id.license_plate or '', fmt['cell'])

            # Separate Trailer Columns
            sheet.write(row, 5, p.trailer_1_id.license_plate or '', fmt['cell'])
            sheet.write(row, 6, p.trailer_2_id.license_plate or '', fmt['cell'])

            sheet.write(row, 7, p.product_id.name or '', fmt['cell'])
            sheet.write(row, 8, p.total_compartments or 0.0, fmt['number'])

            comps = [p.compartment_1, p.compartment_2, p.compartment_3, p.compartment_4,
                     p.compartment_5, p.compartment_6, p.compartment_7, p.compartment_8, p.compartment_9]
            for i, val in enumerate(comps):
                sheet.write(row, 9 + i, val or 0, fmt['number'])
            row += 1