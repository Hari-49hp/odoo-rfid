# -*- coding: utf-8 -*-

from odoo import http
from odoo.http import request
from odoo.exceptions import UserError
from odoo import api, fields, models ,_
import requests
import json
import logging

_logger = logging.getLogger(__name__)
HEADERS = {'Content-Type': 'application/json'}


class rfid(http.Controller):

    @http.route('/api/create/rfid_ser', type='json', methods=['POST'], auth='public', sitemap=False)
    def create_rfid_ser(self, **kw):
        _logger.info("000000000000000000000000 %s ", kw.get('default_code',False))
        if kw and kw.get('default_code',False):
            product_id=request.env['product.product'].sudo().search([('default_code','=',kw.get('default_code'))])
            rfid_ser=request.env['rfid.ser'].sudo().create(kw)
            _logger.info("1111111111111111111111111111 %s ", rfid_ser)
            rfid_ser.product_id = product_id.id if product_id else False
            _logger.info("22222222222222222222222222 %s ", rfid_ser.product_id)

    @http.route('/api/printed/rfid_ser', type='json', methods=['POST'], auth='public', sitemap=False)
    def printed_rfid_ser(self, **kw):
        if kw:
            rfid_ser=request.env['rfid.ser'].sudo().search([('lot_serial_no','in',kw.get('lot_serial_no',[]))])
            rfid_ser.update({
                'print_status': "printed"
            })

    @http.route('/api/git/rfid_ser', type='json', methods=['POST'], auth='public', sitemap=False)
    def git_rfid_ser(self, **kw):
        if kw:
            domain=[('status','!=','done'),('print_status','=','printed')]
            # domain=[]
            N=None
            if kw.get('next_serial_count',False):
                N=kw.get('next_serial_count',False)
            _logger.info("333333333333333333333333 %s ", kw.get('default_code',False))
            if kw.get('default_code',False):
                domain.append(('default_code','=',kw.get('default_code',False)))
            rfid_ser=request.env['rfid.ser'].sudo().search(domain,limit=N)
            rfid_ser.sudo().update({
                'status': 'done',
            })
            _logger.info("444444444444444444444444444444444444444 %s ", rfid_ser)
            data=list(rfid_ser.mapped('lot_serial_no'))
            _logger.info("5555555555555555555555555555555555555555 %s ", data)
            return {'data':data}

    @http.route('/api/rfid_pos_get_tags_info', type='json', methods=['POST'], auth='public', sitemap=False,cors='*')
    def rfid_pos_get_tags_info(self, DeviceSerialNumberSale=None,returns=None,sales= None):
        _logger.info("rfid_pos_get_tags_info %s , %s",returns,sales)
        values = {}
        serials = []
        conf = request.env['ir.config_parameter'].sudo()
        client_side_url = conf.get_param('client_side_url')
        if DeviceSerialNumberSale:
            _logger.info("DeviceSerialNumberSale %s ", DeviceSerialNumberSale)
            if sales:
                _logger.info("sales %s ", sales)
                tags=request.env['rfid.tagsinfo'].sudo().search([('DeviceSerialNumber','=',DeviceSerialNumberSale),('DeactvatedEPC','!=',False),('active','=',False)]).filtered(lambda x : len(x.ReactvatedEPC) < 4)
                for tag in tags:
                    _logger.info("tag %s ", tag)
                    serials.append({
                            "EPC": tag.EPC,
                            "IDS": tag.IDS,
                            "DeviceID": tag.DeviceID,
                            "DeviceSerialNumber": tag.DeviceSerialNumber,
                            "TagState": tag.TagState,
                            "DeactvatedEPC": tag.DeactvatedEPC,
                            "ReactvatedEPC": tag.ReactvatedEPC,
                            "TID": tag.TID,
                            "DataSource": tag.DataSource,
                            "DecodedData": tag.DecodedData,
                            "TagSerialNumber": tag.TagSerialNumber,
                            "DateTime": tag.DateTime,
                            # "active": tag.active,
                            "state": tag.state,
                            "id": tag.id
                        })
                tags_returned = request.env['rfid.tagsinfo'].sudo().search([('DeviceSerialNumber', '=', DeviceSerialNumberSale),('ReactvatedEPC', '!=', False),('active','=',False)]).filtered(lambda x : len(x.DeactvatedEPC) < 4)
                for tag_return in tags_returned:
                    if not client_side_url:
                        raise UserError(_("Please add Client side url"))
                    if DeviceSerialNumberSale:
                        serial_returned = {
                            "EPC": tag_return.EPC,
                            "IDS": tag_return.IDS,
                            "DeviceID": tag_return.DeviceID,
                            "DeviceSerialNumber": tag_return.DeviceSerialNumber,
                            "TagState": tag_return.TagState,
                            "DeactvatedEPC": tag_return.DeactvatedEPC,
                            "ReactvatedEPC": tag_return.ReactvatedEPC,
                            "TID": tag_return.TID,
                            "DataSource": tag_return.DataSource,
                            "DecodedData": tag_return.DecodedData,
                            "TagSerialNumber": tag_return.TagSerialNumber,
                            "DateTime": tag_return.DateTime,
                            # "active": tag_return.active,
                            "state": 'returned',
                        }
                        url = str(client_side_url) + '/api/add_to_rfid_pos_checklist'
                        values = {'serial': serial_returned}
                        response = requests.post(url, data=json.dumps({"params": values}), headers=HEADERS)
                        # if response:
                        #     # _logger.info("response %s , %s ",response,response.text)
                        #     tag_return.sudo().update({'active': False})
            if returns:
                _logger.info("returns %s ", returns)
                tags = request.env['rfid.tagsinfo'].sudo().search([('DeviceSerialNumber', '=', DeviceSerialNumberSale), ('ReactvatedEPC', '!=', False),('active','=',False)]).filtered(lambda x : len(x.DeactvatedEPC) < 4)
                for tag in tags:
                    _logger.info("tag %s ", tag)
                    serials.append({
                        "EPC": tag.EPC,
                        "IDS": tag.IDS,
                        "DeviceID": tag.DeviceID,
                        "DeviceSerialNumber": tag.DeviceSerialNumber,
                        "TagState": tag.TagState,
                        "DeactvatedEPC": tag.DeactvatedEPC,
                        "ReactvatedEPC": tag.ReactvatedEPC,
                        "TID": tag.TID,
                        "DataSource": tag.DataSource,
                        "DecodedData": tag.DecodedData,
                        "TagSerialNumber": tag.TagSerialNumber,
                        "DateTime": tag.DateTime,
                        # "active": tag.active,
                        "state": tag.state,
                        "id": tag.id
                    })

                tags_not_sold = request.env['rfid.tagsinfo'].sudo().search([('DeviceSerialNumber', '=', DeviceSerialNumberSale), ('DeactvatedEPC', '!=', False),('active','=',False)]).filtered(lambda x : len(x.ReactvatedEPC) < 4)
                for tag_not_sold in tags_not_sold:
                    if not client_side_url:
                        raise UserError(_("Please add Client side url"))
                    if DeviceSerialNumberSale:
                        serial_not_sold = {
                            "EPC": tag_not_sold.EPC,
                            "IDS": tag_not_sold.IDS,
                            "DeviceID": tag_not_sold.DeviceID,
                            "DeviceSerialNumber": tag_not_sold.DeviceSerialNumber,
                            "TagState": tag_not_sold.TagState,
                            "DeactvatedEPC": tag_not_sold.DeactvatedEPC,
                            "ReactvatedEPC": tag_not_sold.ReactvatedEPC,
                            "TID": tag_not_sold.TID,
                            "DataSource": tag_not_sold.DataSource,
                            "DecodedData": tag_not_sold.DecodedData,
                            "TagSerialNumber": tag_not_sold.TagSerialNumber,
                            "DateTime": tag_not_sold.DateTime,
                            # "active": tag_not_sold.active,
                            "state": 'not_sold',
                        }
                        url = str(client_side_url) + '/api/add_to_rfid_pos_checklist'
                        values = {'serial': serial_not_sold}
                        response = requests.post(url, data=json.dumps({"params": values}), headers=HEADERS)
                        # if response:
                        #     # _logger.info("response %s , %s ",response,response.text)
                        #     tag_return.sudo().update({'active': False})
            values["serials"] = serials
            _logger.info("values %s ", values)
        return values

    @http.route('/api/rfid_return_pos', type='json', methods=['POST'], auth='public', sitemap=False)
    def rfid_return_pos(self, DeviceSerialNumberReturn=None):
        values = {}
        serials = []
        if DeviceSerialNumberReturn:
            tags = request.env['rfid.tagsinfo'].sudo().search([('DeviceSerialNumber', '=', DeviceSerialNumberReturn), ('active', '=', False)])
            for tag in tags:
                serials.append(tag.EPC)
                # tag.sudo().update({'active': False})
            values["serials"] = serials
        return values

    @http.route('/api/remove_tags_info_serverside', type='json', methods=['POST'], auth='public', sitemap=False)
    def remove_tags_info_serverside(self, tags=None):
        for tag in tags:
            tags = request.env['rfid.tagsinfo'].sudo().search([('id', '=', tag['tag_id']),('active','=',False)])
            tags.sudo().update({'active': True})
        return True

    @http.route('/api/get/tags', type='json', methods=['POST'], auth='public', sitemap=False)
    def get_tags(self,**kw):
        lots = request.env['tags.adjust'].sudo().search([("active","=",False)])
        lots.sudo().update({
            "active":True
        })
        lot_names = lots.mapped('EPC')
        return lot_names
