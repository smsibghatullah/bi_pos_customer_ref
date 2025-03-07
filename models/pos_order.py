from odoo import models, fields,api, _
import qrcode
import base64
from io import BytesIO

class AccountMove(models.Model):
    _inherit = 'account.move'

    customer_reference = fields.Char(string='Customer Reference')
    qr_code = fields.Binary("QR Code", compute='_generate_qr_code')

    def _generate_qr_code(self, **kwargs):
        for rec in self:
            if qrcode and base64:
                qr = qrcode.QRCode(
                    version=1,
                    error_correction=qrcode.constants.ERROR_CORRECT_L,
                    box_size=3,
                    border=4,
                )
                qr.add_data(f"https://linktr.ee/akg_hardware")
                qr.make(fit=True)
                
                img = qr.make_image(fill_color="black", back_color="white")
                temp = BytesIO()
                img.save(temp, format="PNG")
                qr_image = base64.b64encode(temp.getvalue())

                rec.qr_code = qr_image


class PosOrder(models.Model):
    _inherit = 'pos.order'

    customer_reference = fields.Char(string='Customer Reference')


    def _order_fields(self, ui_order):
        """ Prepare dictionary for create method """
        result = super()._order_fields(ui_order)
        result['customer_reference'] = ui_order.get('customer_reference')
        return result


    def _create_invoice(self, move_vals):
        self.ensure_one()
        print(self.name,"OOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOO333333333333333333333333333333333333333333OOOOOOOOOOOOOOOOOOOOOO",move_vals)
        new_move = self.env['account.move'].sudo().with_company(self.company_id).with_context(default_move_type=move_vals['move_type']).create(move_vals)
        print(self.customer_reference,"errrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrr",new_move)
        new_move.customer_reference = self.customer_reference
        message = _(
            "This invoice has been created from the point of sale session: %s",
            self._get_html_link(),
        )
        new_move.message_post(body=message)
        if self.config_id.cash_rounding:
            rounding_applied = float_round(self.amount_paid - self.amount_total,
                                           precision_rounding=new_move.currency_id.rounding)
            rounding_line = new_move.line_ids.filtered(lambda line: line.display_type == 'rounding')
            if rounding_line and rounding_line.debit > 0:
                rounding_line_difference = rounding_line.debit + rounding_applied
            elif rounding_line and rounding_line.credit > 0:
                rounding_line_difference = -rounding_line.credit + rounding_applied
            else:
                rounding_line_difference = rounding_applied
            if rounding_applied:
                if rounding_applied > 0.0:
                    account_id = new_move.invoice_cash_rounding_id.loss_account_id.id
                else:
                    account_id = new_move.invoice_cash_rounding_id.profit_account_id.id
                if rounding_line:
                    if rounding_line_difference:
                        rounding_line.with_context(skip_invoice_sync=True, check_move_validity=False).write({
                            'debit': rounding_applied < 0.0 and -rounding_applied or 0.0,
                            'credit': rounding_applied > 0.0 and rounding_applied or 0.0,
                            'account_id': account_id,
                            'price_unit': rounding_applied,
                        })

                else:
                    self.env['account.move.line'].with_context(skip_invoice_sync=True, check_move_validity=False).create({
                        'balance': -rounding_applied,
                        'quantity': 1.0,
                        'partner_id': new_move.partner_id.id,
                        'move_id': new_move.id,
                        'currency_id': new_move.currency_id.id,
                        'company_id': new_move.company_id.id,
                        'company_currency_id': new_move.company_id.currency_id.id,
                        'display_type': 'rounding',
                        'sequence': 9999,
                        'name': self.config_id.rounding_method.name,
                        'account_id': account_id,
                    })
            else:
                if rounding_line:
                    rounding_line.with_context(skip_invoice_sync=True, check_move_validity=False).unlink()
            if rounding_line_difference:
                existing_terms_line = new_move.line_ids.filtered(
                    lambda line: line.account_id.account_type in ('asset_receivable', 'liability_payable'))
                if existing_terms_line.debit > 0:
                    existing_terms_line_new_val = float_round(
                        existing_terms_line.debit + rounding_line_difference,
                        precision_rounding=new_move.currency_id.rounding)
                else:
                    existing_terms_line_new_val = float_round(
                        -existing_terms_line.credit + rounding_line_difference,
                        precision_rounding=new_move.currency_id.rounding)
                existing_terms_line.with_context(skip_invoice_sync=True).write({
                    'debit': existing_terms_line_new_val > 0.0 and existing_terms_line_new_val or 0.0,
                    'credit': existing_terms_line_new_val < 0.0 and -existing_terms_line_new_val or 0.0,
                })
        return new_move

class ResCountry(models.Model):
    _inherit = 'res.country'

    qr_code_akg = fields.Binary("QR Code", compute='_generate_qr_code')

    def _generate_qr_code(self, **kwargs):
        for rec in self:
            if qrcode and base64:
                qr = qrcode.QRCode(
                    version=1,
                    error_correction=qrcode.constants.ERROR_CORRECT_L,
                    box_size=3,
                    border=4,
                )
                qr.add_data(f"https://linktr.ee/akg_hardware")
                qr.make(fit=True)
                
                img = qr.make_image(fill_color="black", back_color="white")
                temp = BytesIO()
                img.save(temp, format="PNG")
                qr_image = base64.b64encode(temp.getvalue())

                rec.qr_code_akg = qr_image

class BaseDocumentLayout(models.TransientModel):
    _inherit = 'base.document.layout'

    qr_code_akg = fields.Binary("QR Code", compute='_generate_qr_code', store=True)

    def _generate_qr_code(self, **kwargs):
        for rec in self:
            if qrcode and base64:
                qr = qrcode.QRCode(
                    version=1,
                    error_correction=qrcode.constants.ERROR_CORRECT_L,
                    box_size=3,
                    border=4,
                )
                qr.add_data(f"https://linktr.ee/akg_hardware")
                qr.make(fit=True)
                
                img = qr.make_image(fill_color="black", back_color="white")
                temp = BytesIO()
                img.save(temp, format="PNG")
                qr_image = base64.b64encode(temp.getvalue())

                rec.qr_code_akg = qr_image


