# -*- coding: utf-8 -*-

from odoo import models, fields, api

class POSConfig(models.Model):
    _inherit = 'pos.config'

    DeviceSerialNumberSale = fields.Char('Device Serial Number Sales')
    DeviceSerialNumberReturn = fields.Char('Device Serial Number Returns')

# class tags(models.Model):
#     _name = 'tags'
#     _rec_name = "EPC"
#     DateTimeUTC = fields.Date(string="", required=False, )
#     Channel = fields.Char(string="", required=False, )
#     TID = fields.Char(string="", required=False, )
#     EPC = fields.Char(string="", required=True, )
#     DeviceName = fields.Char(string="", required=False, )
#     DeviceLocation = fields.Char(string="", required=False, )
#     AntennaLocation = fields.Char(string="", required=False, )
#     Direction = fields.Char(string="", required=False, )
#     Event = fields.Char(string="", required=False, )
#     Transition = fields.Char(string="", required=False, )
#     FirstSector = fields.Char(string="", required=False, )
#     LastSector = fields.Char(string="", required=False, )
#     active = fields.Boolean('Active', default=True)





