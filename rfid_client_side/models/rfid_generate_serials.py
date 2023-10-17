# -*- coding: utf-8 -*-

from odoo import models, fields, api, exceptions,_
from odoo.exceptions import UserError
import requests
import json


class RfidSerGenerate(models.TransientModel):
    _name = 'rfid.ser.generate'
    _rec_name = 'name'
    _description = 'RFID Serials'

    product_id = fields.Many2one(comodel_name="product.product", string="Product", required=True, )
    name = fields.Char(string="Description", required=False, )
    default_code = fields.Char(string="Internal Ref", required=False, )
    barcode = fields.Char(string="Barcode", required=False, )
    sequence_no = fields.Integer(string="Seq No To Generate", required=False, )

    @api.onchange('product_id')
    def get_product_info(self):
        self.name = self.product_id.name
        self.default_code = self.product_id.default_code or False
        self.barcode = self.product_id.barcode or False

    def generate_rfid_sequences(self):
        if self.sequence_no <= 0:
            raise exceptions.ValidationError('You must valid number in ( Seq No To Generate ) field.')
        rfid_ser = self.env['rfid.ser']
        conf = self.env['ir.config_parameter'].sudo()
        server_side_url = str(conf.get_param('server_side_url'))
        if server_side_url == 'False':
            raise UserError(_("Please add server side url"))
        url = server_side_url + '/api/create/rfid_ser'
        headers = {
            "Content-Type": "application/json",
        }
        for rec in range(self.sequence_no):
            values = {'product_id': self.product_id.id,
                      'name': self.name,
                      'default_code': self.default_code,
                      'barcode': self.barcode, }
            rfid_rec = rfid_ser.sudo().create(values)

            values = {
                'product_id_id': self.product_id.id,
                # 'product_id': self.product_id.id,
                'name': self.name,
                'default_code': self.default_code,
                'lot_serial_no': rfid_rec.lot_serial_no,
                'barcode': self.barcode, }
            response = requests.post(url, data=json.dumps({"params": values}), headers=headers)



class ResConfigSettings(models.TransientModel):
    _inherit = 'res.config.settings'

    server_side_url = fields.Char('Server Side URL')
    template_name = fields.Char('Template name')
    print_qty = fields.Integer('Print Qty')
    printer_name = fields.Char('Printer Name')

    def set_values(self):
        obj = self.env['ir.config_parameter'].sudo()
        obj.set_param('server_side_url', self.server_side_url)
        obj.set_param('template_name', self.template_name)
        obj.set_param('print_qty', self.print_qty)
        obj.set_param('printer_name', self.printer_name)
        super(ResConfigSettings, self).set_values()

    def get_values(self):
        res = super(ResConfigSettings, self).get_values()
        conf = self.env['ir.config_parameter'].sudo()
        res.update(
            server_side_url=str(conf.get_param('server_side_url')),
        )
        res.update(
            template_name=str(conf.get_param('template_name')),
        )
        res.update(
            print_qty=int(conf.get_param('print_qty')),
        )
        res.update(
            printer_name=str(conf.get_param('printer_name')),
        )
        return res

