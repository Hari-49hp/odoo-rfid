from odoo import api, fields, models, _
from odoo.exceptions import UserError, ValidationError
import requests
import json
import pandas as pd
import os
import logging
_logger = logging.getLogger(__name__)


class stock_move(models.Model):
    _inherit = 'stock.move'

    def import_rfid(self):
        values = {'product_id_id': self.product_id.id,
                  'next_serial_count': self.next_serial_count, }
        headers = {"Content-Type": "application/json", }
        conf = self.env['ir.config_parameter'].sudo()
        server_side_url = str(conf.get_param('server_side_url'))
        if server_side_url == 'False':
            raise UserError(_("Please add server side url"))
        url = server_side_url + '/api/git/rfid_ser'
        response = requests.post(url, data=json.dumps({"params": values}), headers=headers)
        lot_names = response.json().get('result').get('data', [])
        rfid_ser = self.env['rfid.ser'].sudo().search([('name', 'in', lot_names)])
        rfid_ser.sudo().update({
            'status': 'done',
        })
        move_lines_commands = self._generate_serial_move_line_commands(lot_names)
        self.write({'move_line_ids': move_lines_commands})
        self.env.cr.commit()
        raise UserError(_("Please refresh page"))
        # return self.action_show_details()


class stock_inventory_line(models.Model):
    _inherit = 'stock.inventory.line'

    is_import = fields.Boolean(string="", )


class NewModule(models.Model):
    _inherit = 'stock.inventory'

    def delete_date(self, stock_inventory_id=False):
        rec = self.browse(stock_inventory_id or self.id)
        for line in rec.line_ids:
            if line.is_import:
                line.product_qty = 0
        self.env.cr.commit()
        raise UserError(_("Please refresh page"))

    def get_adjustments(self, stock_inventory_id=False):
        rec = self.browse(stock_inventory_id or self.id)
        # lots = self.env['tags'].sudo().search([])
        # lot_names = lots.mapped('EPC')
        headers = {"Content-Type": "application/json", }
        conf = self.env['ir.config_parameter'].sudo()
        server_side_url = str(conf.get_param('server_side_url'))
        if server_side_url == 'False':
            raise ValidationError(_("Please add server side url"))
        url = server_side_url + '/api/get/tags'
        response = requests.post(url, data=json.dumps({"params": {}}), headers=headers)
        lot_names = False
        if response.status_code == 200:
            lot_names = response.json().get('result')
        if lot_names:
            rec.sudo().create_lines(lot_names, rec)
        self.env.cr.commit()
        raise UserError(_("Please refresh page"))

    @api.model
    def update_orderline_state(self, stock_inventory_id=False):

        rec = self.browse(stock_inventory_id)
        if rec:
            if len(rec.location_ids.ids) != 1:
                raise UserError(_("Please choose one location"))
            if rec.product_ids:
                for product in rec.product_ids:
                    lot_names = rec.get_lot_names(product=product.id)
                    rec.sudo().create_lines(lot_names, rec)
            else:
                lot_names = rec.get_lot_names()
                rec.sudo().create_lines(lot_names, rec)
            self.env.cr.commit()
            raise UserError(_("Please refresh page"))

    def get_lot_names(self, product=None):
        values = {'product_id_id': product, }
        headers = {"Content-Type": "application/json", }
        conf = self.env['ir.config_parameter'].sudo()
        server_side_url = str(conf.get_param('server_side_url'))
        if server_side_url == 'False':
            raise ValidationError(_("Please add server side url"))
        url = server_side_url + '/api/git/rfid_ser'
        response = requests.post(url, data=json.dumps({"params": values}), headers=headers)
        lot_names = []
        if response.status_code == 200:
            lot_names = response.json().get('result').get('data', [])
        return lot_names

    def create_lines(self, lot_names, adjustments):
        line_ids = []
        for lot_name in lot_names:
            product_not_returned = []
            product_ser = self.env['rfid.ser'].sudo().search([('lot_serial_no', '=', lot_name)], limit=1)
            lot = self.env['stock.production.lot'].sudo().search([('name', '=', lot_name)], limit=1)
            if not lot and product_ser:
                lot = self.env['stock.production.lot'].sudo().create({
                    'name': lot_name,
                    'product_id': product_ser.product_id.id,
                    'company_id': self.company_id.id,
                })
            line_adjustments = self.env['stock.inventory.line'].sudo().search(
                [("prod_lot_id", '=', lot.id), ("inventory_id", "=", adjustments.id)], limit=1)
            if line_adjustments:
                line_adjustments.product_qty = 1
            else:
                if product_ser:
                    line_ids.append((0, 0, {
                        'product_id': product_ser.product_id.id,
                        'location_id': self.location_ids.ids[0],
                        'prod_lot_id': lot.id,
                        'product_qty': 1,
                        'is_import': True,
                    }))
                elif lot:
                    line_ids.append((0, 0, {
                        'product_id': lot.product_id.id,
                        'location_id': self.location_ids.ids[0],
                        'prod_lot_id': lot.id,
                        'product_qty': 1,
                        'is_import': True,
                    }))
                else:
                    if not self.env['items.added.inventory'].search(
                            [('inventory_adjustments_id', '=', adjustments.id),
                             ('location_id', '=', adjustments.location_ids[0].id),
                             ('lot_name', '=', lot_name)]):
                        self.env['items.added.inventory'].create({
                            "inventory_adjustments_id": adjustments.id,
                            "lot_name": lot_name,
                            "location_id": adjustments.location_ids[0].id
                        })
        if line_ids:
            self.line_ids = line_ids

class stock_location(models.Model):
    _inherit = 'stock.location'

    path_file = fields.Char(string="Inventory Adjustments Path", required=False, )


class ItemsAddedInventory(models.Model):
    _name = 'items.added.inventory'
    _rec_name = 'lot_name'
    _description = 'New Description'

    inventory_adjustments_id = fields.Many2one('stock.inventory', )
    lot_name = fields.Char(string="Lot/Serial Number", )
    location_id = fields.Many2one('stock.location', 'Location', required=True, )
