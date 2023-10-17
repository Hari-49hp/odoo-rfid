# -*- coding: utf-8 -*-

from odoo import models, fields, api

class RfidSer(models.Model):
    _name = 'rfid.ser'
    _rec_name = 'name'
    _description = 'RFID Serials'

    product_id = fields.Many2one(comodel_name="product.product", string="Product", required=False, )
    product_id_id = fields.Integer(string="Product_id", required=False, )
    name = fields.Char(string="Description", required=False, )
    default_code = fields.Char(string="Internal Ref", required=False, )
    barcode = fields.Char(string="Barcode", required=False, )
    lot_serial_no = fields.Char(string="Lot/Serial No", required=False,readonly=True,copy=False )
    status = fields.Selection(string="status", selection=[('draft', 'Draft'), ('done', 'Done'), ], required=False,default='draft' )
    print_status = fields.Selection(string="Print status", selection=[('new', 'NEW'), ('printed', 'Printed'), ], required=False,default='new' )

    @api.onchange('product_id')
    def get_product_info(self):
        self.name = self.product_id.name
        self.default_code = self.product_id.default_code or False
        self.barcode = self.product_id.barcode or False

    @api.model
    def create(self, vals):
        record_name = "/"
        sequence_id = self.env.ref("rfid_server_side.rfid_sequence").id
        if sequence_id:
            record_name = self.env['ir.sequence'].browse(sequence_id).next_by_id()
        if not vals.get('lot_serial_no',False):
            vals.update({"lot_serial_no": str(record_name)})
        return super(RfidSer, self).create(vals)

class RFIDTagsInfo(models.Model):
    _name = 'rfid.tagsinfo'
    _description = 'RFID Tags Info'
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
    state = fields.Selection(string="Status", selection=[('draft', 'Draft'), ('sold', 'Sold'),('not_sold', 'Not Sold'),('returned', 'Returned'),('not_found', 'Not Found'), ], required=False )
    # channel = fields.Char(string="Channel", required=False, )
    # device_location = fields.Char(string="Device Location", required=False, )
    # antenna = fields.Char(string="Antenna", required=False, )
    # antenna_location = fields.Char(string="Antenna Location", required=False, )
    # direction = fields.Char(string="Direction", required=False, )
    # event = fields.Char(string="Event", required=False, )
    # transition = fields.Char(string="Transition", required=False, )
    # first_sector = fields.Char(string="First Sector", required=False, )
    # last_sector = fields.Char(string="Last Sector", required=False, )
    # x = fields.Char(string="X", required=False, )
    # y = fields.Char(string="Y", required=False, )


class ResConfigSettings(models.TransientModel):
    _inherit = 'res.config.settings'

    client_side_url = fields.Char('CLient Side URL')

    def set_values(self):
        obj = self.env['ir.config_parameter'].sudo()
        obj.set_param('client_side_url', self.client_side_url)
        super(ResConfigSettings, self).set_values()

    def get_values(self):
        res = super(ResConfigSettings, self).get_values()
        conf = self.env['ir.config_parameter'].sudo()
        res.update(client_side_url=str(conf.get_param('client_side_url')),)
        return res




class tags(models.Model):
    _name = 'tags.adjust'
    _rec_name = "EPC"

    DateTimeUTC = fields.Date(string="", required=False, )
    Channel = fields.Text(string="", required=False, )
    TID = fields.Text(string="", required=False, )
    EPC = fields.Text(string="", required=True, )
    DeviceId = fields.Text(string="", required=False, )
    DeviceName = fields.Text(string="", required=False, )
    DeviceLocation = fields.Text(string="", required=False, )
    Antenna = fields.Integer(string="", required=False, )
    AntennaLocation = fields.Text(string="", required=False, )
    Direction = fields.Text(string="", required=False, )
    Event = fields.Text(string="", required=False, )
    Transition = fields.Text(string="", required=False, )
    FirstSector = fields.Integer(string="", required=False, )
    LastSector = fields.Integer(string="", required=False, )
    X = fields.Integer(string="", required=False, )
    Y = fields.Integer(string="", required=False, )
    active = fields.Boolean('Active')







