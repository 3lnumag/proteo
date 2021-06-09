# -*- coding: utf-8 -*-

from odoo import fields, models, api
from odoo.exceptions import UserError

import requests
import json
import logging

_logger = logging.getLogger(__name__)

class MrpProduction(models.Model):
   _inherit = 'mrp.production'

   asys = fields.Boolean('ASYS', default=False, copy=False)

   def enviar(self):

      url = self.env.ref('conector_mrp.url_mrp').sudo().value
      api_key = self.env.ref('conector_mrp.api_key_mrp').sudo().value

      headers = {
         'x-api-key': api_key,
         'content-type': 'application/json'
      }
      data = self._data()
      _logger.info(data)

      response = requests.post(url, data=json.dumps(data), headers=headers)
      _logger.info(response)

      if response.status_code == requests.codes.ok:
         pass
      else:
         raise UserError("Error de conexión:\n%s" % response)

   def _data(self):
      dic = {}
      components = []

      dic['id_op'] = self.id
      dic['no_op'] = self.name
      dic['product_produce'] = self.product_id.name
      dic['product_code_produce'] = self.product_id.default_code
      dic['quantity_produce'] = self.product_qty


      for l in self.move_raw_ids:
         dic2 = {}
         dic2['product_name'] = l.product_id.name
         dic2['product_code'] = l.product_id.default_code
         dic2['target_weight'] = l.product_uom_qty
         components.append(dic2)

      dic['components'] = components

      return dic