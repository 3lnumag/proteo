# -*- coding: utf-8 -*-

from odoo import fields, models
from odoo.tools.misc import format_date, OrderedSet


class StockMove(models.Model):
   _inherit = 'stock.move'

   # def _action_cancel(self):
   #    self.write({
   #       'state': 'cancel'
   #    })
   #    return True

   # def _do_unreserve(self):
   #    moves_to_unreserve = OrderedSet()
   #    for move in self:
   #       if move.state == 'cancel' or (move.state == 'done' and move.scrapped):
   #          # We may have cancelled move in an open picking in a "propagate_cancel" scenario.
   #          # We may have done move in an open picking in a scrap scenario.
   #          continue
   #       # elif move.state == 'done':
   #       #     raise UserError(_("You cannot unreserve a stock move that has been set to 'Done'."))
   #       moves_to_unreserve.add(move.id)
   #    moves_to_unreserve = self.env['stock.move'].browse(moves_to_unreserve)
   #
   #    ml_to_update, ml_to_unlink = OrderedSet(), OrderedSet()
   #    moves_not_to_recompute = OrderedSet()
   #    for ml in moves_to_unreserve.move_line_ids:
   #       if ml.qty_done:
   #          ml_to_update.add(ml.id)
   #       else:
   #          ml_to_unlink.add(ml.id)
   #          moves_not_to_recompute.add(ml.move_id.id)
   #    ml_to_update, ml_to_unlink = self.env['stock.move.line'].browse(
   #       ml_to_update), self.env['stock.move.line'].browse(ml_to_unlink)
   #    moves_not_to_recompute = self.env['stock.move'].browse(
   #       moves_not_to_recompute)
   #
   #    ml_to_update.write({'product_uom_qty': 0})
   #    ml_to_unlink.unlink()
   #    # `write` on `stock.move.line` doesn't call `_recompute_state` (unlike to `unlink`),
   #    # so it must be called for each move where no move line has been deleted.
   #    (moves_to_unreserve - moves_not_to_recompute)._recompute_state()
   #    return True
