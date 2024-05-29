from odoo import models, fields,api

class PosOrder(models.Model):
    _inherit = 'pos.order'

    customer_reference = fields.Char(string='Customer Reference')

    @api.model
    def set_customer_reference(self,order_id, payload):
        order = self.env['pos.order'].search([], limit=1)
        if order:
            order.write({'customer_reference': payload})