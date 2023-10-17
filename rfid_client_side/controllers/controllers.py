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

    @http.route('/api/rfid_get_serials_pos', type='json', methods=['POST'], auth='public', sitemap=False)
    def rfid_get_serials_pos(self, DeviceSerialNumberSale=None, server_side_url=None,returns=None,sales= None ):
        values = {}
        if not server_side_url:
            raise UserError(_("Please add server side url"))
        if DeviceSerialNumberSale:
            url = server_side_url + '/api/rfid_pos_get_tags_info'
            values = {'DeviceSerialNumberSale': DeviceSerialNumberSale,'returns':returns,'sales': sales}
            response = requests.post(url, data=json.dumps({"params": values}), headers=HEADERS)
            if response and response.json().get('result',''):
                values = {'serials': response.json().get('result').get('serials', [])}
        return values

    @http.route('/api/rfid_get_products_pos', type='json', methods=['POST'], auth='public', sitemap=False)
    def rfid_get_products_pos(self, serials=None,session_id=None,returns=None,sales=None):
        _logger.info("rfid_get_products_pos %s", serials)
        values = {}
        products = []
        if serials:
            for ser in serials:
                domain = []
                if sales:
                    domain = [('lot_id.product_qty', '=', 1),('lot_id.name', '=', ser['EPC']),]
                if returns:
                    domain = [('lot_id.product_qty', '=', 0),('lot_id.name', '=', ser['ReactvatedEPC']),]

                products_recs = request.env['stock.quant'].sudo().search(domain,limit=1)
                if products_recs:
                    if products:
                        found = False
                        for pro in products:
                            if pro['product_id'] == products_recs.product_id.id:
                                if sales:
                                    pro['EPC'].append({'lot_name': ser['EPC']})
                                if returns:
                                    pro['EPC'].append({'lot_name': ser['ReactvatedEPC']})

                                pro['tag_id'].append(ser['id'])
                                found = True
                        if not found:
                            if sales:
                                products.append({'product_id': products_recs.product_id.id, 'tag_id': [ser['id']],'EPC': [{'lot_name': ser['EPC']}]})
                            if returns:
                                products.append({'product_id': products_recs.product_id.id, 'tag_id': [ser['id']],'EPC': [{'lot_name': ser['ReactvatedEPC']}]})

                    else:
                        if sales:
                            products.append({'product_id' : products_recs.product_id.id,'tag_id':[ser['id']],'EPC':[{'lot_name': ser['EPC']}]})
                        if returns:
                            products.append({'product_id': products_recs.product_id.id, 'tag_id': [ser['id']],'EPC': [{'lot_name': ser['ReactvatedEPC']}]})
                    # rfid_pos_check_list = request.env['rfid.pos.check.list'].sudo().create(ser)
                else:
                    rfid_pos_check_list = request.env['rfid.pos.check.list'].sudo().create(ser)
                    rfid_pos_check_list.sudo().write({'state': 'not_found','session_id':int(session_id) if session_id else False})

            values["products"] = products
            _logger.info("products %s", products)
        return values

    @http.route('/api/add_to_rfid_pos_checklist', type='json', methods=['POST'], auth='public', sitemap=False)
    def add_to_rfid_pos_checklist(self, serial=None):
        _logger.info("add_to_rfid_pos_checklist %s", serial)
        if serial:
            rfid_pos_check_list = request.env['rfid.pos.check.list'].sudo().create(serial)
        return True

    @http.route('/api/remove_tags_info_clientside', type='json', methods=['POST'], auth='public', sitemap=False)
    def remove_tags_info_clientside(self, tags=None,server_side_url=None):
        values = {}
        if not server_side_url:
            raise UserError(_("Please add server side url"))
        # print("tags_to_remove",tags)
        if tags:
            url = server_side_url + '/api/remove_tags_info_serverside'
            values = {'tags': tags}
            response = requests.post(url, data=json.dumps({"params": values}), headers=HEADERS)
        return values
