# -*- coding: utf-8 -*-

from odoo import fields, models, _
from odoo.exceptions import AccessError, UserError, ValidationError


class PurchaseOrder(models.Model):
   _inherit = 'purchase.order'

   business_line_id = fields.Many2one('lob', 'Línea de negocio', default=lambda
      self: self.env.user.business_line_id.id, tracking=True)

   def button_cancel_ws(self):
      # for order in self:
      #    # for move in order.order_line.mapped('move_ids'):
      #       # if move.state == 'done':
      #       #    raise UserError(
      #       #       _('Unable to cancel purchase order %s as some receptions have already been done.') % (
      #       #          order.name))
      #    # If the product is MTO, change the procure_method of the closest move to purchase to MTS.
      #    # The purpose is to link the po that the user will manually generate to the existing moves's chain.
      #    if order.state in ('draft', 'sent', 'to approve', 'purchase'):
      #       for order_line in order.order_line:
      #          order_line.move_ids._action_cancel()
      #          if order_line.move_dest_ids:
      #             move_dest_ids = order_line.move_dest_ids
      #             if order_line.propagate_cancel:
      #                move_dest_ids._action_cancel()
      #             else:
      #                move_dest_ids.write({'procure_method': 'make_to_stock'})
      #                move_dest_ids._recompute_state()
      #
      #    for pick in order.picking_ids.filtered(lambda r: r.state != 'cancel'):
      #       pick.action_cancel()
      #
      #    order.order_line.write({'move_dest_ids': [(5, 0, 0)]})

      for order in self:
         for inv in order.invoice_ids:
            if inv and inv.state not in ('cancel', 'draft'):
               raise UserError(
                  _("Unable to cancel this purchase order. You must first cancel the related vendor bills."))

      self.write({'state': 'cancel'})

      self.sudo()._activity_cancel_on_sale()
