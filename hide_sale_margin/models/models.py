# -*- coding: utf-8 -*-

from odoo import models, fields


class SaleReport(models.Model):
    _inherit = 'sale.report'

    margin = fields.Float('Margin', groups="hide_sale_margin.view_sale_margin")
