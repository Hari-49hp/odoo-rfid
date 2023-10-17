# -*- coding: utf-8 -*-

from odoo import models, fields, api,_
from odoo.exceptions import UserError
import requests
import json
import base64




class RfidSer(models.Model):
    _name = 'rfid.ser'
    _rec_name = 'name'
    _description = 'RFID S/api/get/tagserials'

    product_id = fields.Many2one(comodel_name="product.product", string="Product", required=True, )
    product_id_id = fields.Integer(string="Product_id", required=False, )
    name = fields.Char(string="Description", required=False, )
    default_code = fields.Char(string="Internal Ref", required=False, )
    barcode = fields.Char(string="Barcode", required=False, )
    lot_serial_no = fields.Char(string="Lot/Serial No", required=False, readonly=True, copy=False)
    status = fields.Selection(string="status", selection=[('draft', 'Draft'), ('done', 'Done'), ], required=False,
                              default='draft')
    print_status = fields.Selection(string="Print status", selection=[('new', 'NEW'), ('printed', 'Printed'), ],
                                    required=False, default='new')

    @api.onchange('product_id')
    def get_product_info(self):
        self.name = self.product_id.name
        self.default_code = self.product_id.default_code or False
        self.barcode = self.product_id.barcode or False

    @api.model
    def create(self, vals):
        record_name = "/"
        sequence_id = self.env.ref("rfid_client_side.rfid_sequence").id
        if sequence_id:
            record_name = self.env['ir.sequence'].browse(sequence_id).next_by_id()
        if not vals.get("lot_serial_no", False):
            vals.update({"lot_serial_no": str(record_name)})
        return super(RfidSer, self).create(vals)


class print_ser(models.Model):
    _name = 'print.ser'
    _description = 'ser'

    @api.model
    def get_template_name(self):
        conf = self.env['ir.config_parameter'].sudo()
        return str(conf.get_param('template_name'))

    @api.model
    def get_printer_name(self):
        conf = self.env['ir.config_parameter'].sudo()
        return str(conf.get_param('printer_name'))

    @api.model
    def get_print_qty(self):
        conf = self.env['ir.config_parameter'].sudo()
        return  1

    @api.model
    def get_ser_ids(self):
        rfid_ser=self.env['rfid.ser'].sudo().search([('print_status','!=','printed')])
        return [(6, 0, rfid_ser.ids)]

    template_name = fields.Char('Template name', default=get_template_name)
    print_qty = fields.Integer('Print Qty', default=get_print_qty)
    printer_name = fields.Char('Printer Name', default=get_printer_name)
    # filename = fields.Char('Printer Name', default="test.txt")
    ser_ids = fields.Many2many(comodel_name="rfid.ser",default=get_ser_ids)
    txt_file = fields.Binary(string='Txt File',attachment=True)

    def ser_printed(self):
        conf = self.env['ir.config_parameter'].sudo()

        server_side_url = str(conf.get_param('server_side_url'))
        if server_side_url == 'False':
            raise UserError(_("Please add server side url"))
        url = server_side_url + '/api/printed/rfid_ser'
        headers = {
            "Content-Type": "application/json",
        }
        values = {'lot_serial_no':list(self.ser_ids.mapped('lot_serial_no'))}
        self.ser_ids.update({
            "print_status": "printed"
        })
        response = requests.post(url, data=json.dumps({"params": values}), headers=headers)


    def print_text(self):
        for rec in self:
            # rec.ser_ids.update({
            #     'print_status':"printed"
            # })
            rec.ser_printed()
            text="Template name,Product,Price,EPC,PrintQty,Printername"
            for ser in rec.ser_ids:
                text+="\n%s,%s,%s,%s,%s,%s"%(rec.template_name,ser.product_id.name,ser.product_id.list_price,ser.lot_serial_no,rec.print_qty,rec.printer_name)
            rec.txt_file = base64.b64encode(text.encode('utf-8'))
            if rec.txt_file :
                return {
                    'type': 'ir.actions.act_url',
                    'url': "web/content/?model=print.ser&id=" + str(
                        rec.id) + "&filename=Trigger.txt&field=txt_file&download=true",
                    'target': 'self'
                }

class RFIDPosCheckList(models.Model):
    _name = 'rfid.pos.check.list'
    _description = 'RFID Pos CheckList'
    _rec_name = 'EPC'

    IDS = fields.Integer(string="IDS", required=False, )
    DeviceID = fields.Char(string="Device Id", required=False, )
    DeviceSerialNumber = fields.Char(string="Device Serial Number", required=False, )
    TagState = fields.Integer(string="Tag State", required=False, )
    EPC = fields.Char(string="EPC", required=False, )
    DeactvatedEPC = fields.Char(string="Deactvated EPC", required=False, )
    ReactvatedEPC = fields.Char(string="Reactvated EPC", required=False, )
    TID = fields.Char(string="TID", required=False, )
    DataSource = fields.Char(string="DataSource", required=False, )
    DecodedData = fields.Char(string="DecodedData", required=False, )
    TagSerialNumber = fields.Char(string="Tag Serial Number", required=False, )
    DateTime = fields.Char(string="DateTime UTC", required=False, )
    active = fields.Boolean('Active', default=True)
    state = fields.Selection(string="Status", selection=[('draft', 'Draft'), ('sold', 'Sold'),('not_sold', 'Not Sold'),('returned', 'Returned'),('not_found', 'Not Found'), ], required=False,default='draft' )
    session_id = fields.Many2one(comodel_name="pos.session", string="Session", required=False, )