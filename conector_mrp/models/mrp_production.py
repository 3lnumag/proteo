# -*- coding: utf-8 -*-

from odoo import fields, models, api


class MrpProduction(models.Model):
   _inherit = 'mrp.production'

   asys = fields.boolean('ASYS', default=False, copy=False)