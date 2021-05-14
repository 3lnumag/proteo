# -*- coding: utf-8 -*-

from odoo import fields, models, api

from lxml.objectify import fromstring
import base64


class AccountMove(models.Model):
    _inherit = 'account.move'

    project_id = fields.Many2one('account.move.project', "Proyecto",
                                 ondelete="restrict")
    business_line_id = fields.Many2one('lob', 'Línea de negocio', default=lambda
        self: self.env.user.business_line_id.id, tracking=True)

    @api.onchange('partner_id')
    def _resetOrder(self):
        self.l10n_mx_edi_payment_method_id = self.partner_id.payment_method_id.id
        self.l10n_mx_edi_usage = self.partner_id.edi_usage

    @api.model
    def create(self, vals):
        res = super(AccountMove, self).create(vals)
        if vals.get('partner_id') and vals.get('invoice_origin') and vals.get(
                'move_type') == 'out_invoice':
            partner_id = self.env['res.partner'].browse(vals.get('partner_id'))
            res.l10n_mx_edi_payment_method_id = partner_id.payment_method_id.id
            res.l10n_mx_edi_usage = partner_id.edi_usage
            diarios = self.env['account.journal'].search(
                [('type', '=', 'sale'), (
                    'business_line_id', '=', self.env.user.business_line_id.id)])
            if diarios:
                res.journal_id = diarios[0]
        if vals.get('invoice_origin') and vals.get('move_type') == 'in_invoice':
            diarios = self.env['account.journal'].search(
                [('type', '=', 'purchase'), (
                    'business_line_id', '=', self.env.user.business_line_id.id)])
            if diarios:
                res.journal_id = diarios[0]
        return res

    def _l10n_mx_edi_decode_cfdi(self, cfdi_data=None):
        res = super()._l10n_mx_edi_decode_cfdi(cfdi_data=cfdi_data)

        self.ensure_one()

        # Find a signed cfdi.
        if not cfdi_data:
            signed_edi = self._get_l10n_mx_edi_signed_edi_document()
            if signed_edi:
                cfdi_data = base64.decodebytes(
                    signed_edi.attachment_id.with_context(bin_size=False).datas)

        # Nothing to decode.
        if not cfdi_data:
            return {}
        cfdi_node = fromstring(cfdi_data)

        res['folio'] = cfdi_node.get('Folio', cfdi_node.get('folio'))
        res['serie'] = cfdi_node.get('Serie', cfdi_node.get('serie'))
        res['policy'] = cfdi_node.get('metodoPago', cfdi_node.get('MetodoPago'))
        res['method'] = cfdi_node.get('formaPago', cfdi_node.get('FormaPago'))

        return res

    @api.depends('edi_document_ids.attachment_id')
    def _compute_folio(self):
        for move in self:
            cfdi_infos = move._l10n_mx_edi_decode_cfdi()
            move.update({'serie': cfdi_infos.get('serie'),
                         'folio': cfdi_infos.get('folio'),
                         'uuid': cfdi_infos.get('uuid'),
                         'policy': cfdi_infos.get('policy'),
                         'usage': cfdi_infos.get('usage')
                         })
            method = self.env['l10n_mx_edi.payment.method'].search([('code', '=', cfdi_infos.get('method'))])
            if method:
                move.update({'method_id': method.id})

    serie = fields.Char(string='Serie',
                        copy=False, readonly=True,
                        compute='_compute_folio', store=True)
    folio = fields.Char(string='Folio',
                        copy=False, readonly=True,
                        compute='_compute_folio', store=True)
    uuid = fields.Char(string='Uudi',
                       copy=False, readonly=True,
                       compute='_compute_folio', store=True)

    policy = fields.Selection(string='Politica de pago',
                              selection=[('PPD', 'PPD'), ('PUE', 'PUE')],
                              readonly=True, compute='_compute_folio', store=True)

    usage = fields.Selection(
        selection=[
            ('G01', 'Adquisición de mercancías'),
            ('G02', 'Devoluciones, descuentos o bonificaciones'),
            ('G03', 'Gastos en general'),
            ('I01', 'Construcciones'),
            ('I02', 'Mobilario y equipo de oficina por inversiones'),
            ('I03', 'Equipo de transporte'),
            ('I04', 'Equipo de cómputo y accesorios'),
            ('I05', 'Dados, troqueles, moldes, matrices y herramental'),
            ('I06', 'Comunicaciones telefónicas'),
            ('I07', 'Comunicaciones satelitales'),
            ('I08', 'Otra maquinaria y equipo'),
            ('D01', 'Honorarios médicos, dentales y gastos hospitalarios'),
            ('D02', 'Gastos médicos por incapacidad o discapacidad'),
            ('D03', 'Gastos funerales'),
            ('D04', 'Donativos'),
            ('D05',
             'Intereses reales efectivamente pagados por créditos hipotecarios (casa habitación)'),
            ('D06', 'Aportaciones voluntarias al SAR'),
            ('D07', 'Primas por seguros de gastos médicos'),
            ('D08', 'Gastos de transportación escolar obligatoria.'),
            ('D09',
             'Depósitos en cuentas para el ahorro, primas que tengan como base planes de pensiones.'),
            ('D10', 'Pagos por servicios educativos (colegiaturas)'),
            ('P01', 'Por definir'),
        ],
        string="Uso",
        help="Utilizado en CFDI 3.3 para indicar la clave del uso que le dará el receptor a esta factura. Este "
             "valor es definido por el cliente.\nNota: No es motivo de cancelación si la clave configurada no corresponde con el uso "
             "que le dará el receptor del documento.", compute='_compute_folio', readonly=True,
        store=True)

    method_id = fields.Many2one(
        'l10n_mx_edi.payment.method',
        string="Forma de pago", readonly=True,
        help='Indica la forma en que se pagó o se pagará la factura, donde las opciones podrían ser: '
             'Tarjeta de Crédito, etc. Deje vacía si no conoce la forma de pago y el XML mostrará "No Identificado".',
        store=True)

    _sql_constraints = [
        ('uuid_unique', 'UNIQUE(uuid)',
         'Uuid existente')
    ]

    def carga(self):
        self.ensure_one()
        return {
            'name': 'Abrir: Documento Edi',
            'type': 'ir.actions.act_window',
            'res_model': 'document.wizard',
            'view_mode': 'form',
            'context': {'active_id': self.id},
            'target': 'new',
        }

    def button_cancel(self):
        # OVERRIDE
        # Set the electronic document to be canceled and cancel immediately for synchronous formats.
        res = super().button_cancel()

        if self.move_type == "in_invoice" or self.move_type == "in_refund":
            self.edi_document_ids.filtered(lambda doc: doc.attachment_id).write(
                {'state': 'cancelled', 'error': False, 'blocking_level': False})
            self.edi_document_ids._process_documents_no_web_services()

        return res
