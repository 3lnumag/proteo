# -*- coding: utf-8 -*-

from odoo import fields, models, api


class RestPartner(models.Model):
   _inherit = 'res.partner'

   business_line_id = fields.Many2one('lob', 'Línea de negocio', default=lambda
      self: self.env.user.business_line_id.id, tracking=True)

   code = fields.Char('Código')
   legal_representative = fields.Char('Representante legal')

   is_customer = fields.Boolean('Es cliente')
   is_supplier = fields.Boolean('Es proveedor')

   # @api.model
   # def _name_search(self, name, args=None, operator='ilike', limit=100,
   #                  name_get_uid=None):
   #    args = args or []
   #    if name:
   #       args = ['|', '|', ('name', operator, name), ('code', operator, name),
   #               ('legal_representative', operator, name)] + args
   #    return self._search(args, limit=limit, access_rights_uid=name_get_uid)
