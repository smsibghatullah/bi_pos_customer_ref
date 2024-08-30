from odoo import api, models

class PosConfig(models.Model):
    _inherit = 'pos.config'

    @api.model
    def _prepare_ui_config(self):
        ui_config = super(PosConfig, self)._prepare_ui_config()
        ui_config['buttons'].append({
            'name': 'CustomDemoButtons',
            'widget': 'CustomDemoButtons',
        })
        return ui_config
