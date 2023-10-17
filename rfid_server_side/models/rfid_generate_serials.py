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
        for rec in range(self.sequence_no):
            values = {'product_id': self.product_id.id,
                      'name': self.name,
                      'default_code': self.default_code,
                      'barcode': self.barcode, }
            rfid_rec = rfid_ser.sudo().create(values)

