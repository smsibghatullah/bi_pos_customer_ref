odoo.define('pos_button.Custom', function(require) {
    'use strict';
      const { Gui } = require('point_of_sale.Gui');
      const PosComponent = require('point_of_sale.PosComponent');
      const { identifyError } = require('point_of_sale.utils');
      const ProductScreen = require('point_of_sale.ProductScreen');
      const { useListener } = require("@web/core/utils/hooks");
      const Registries = require('point_of_sale.Registries');
      const PaymentScreen = require('point_of_sale.PaymentScreen');
      const { useService } = require("@web/core/utils/hooks");

      class CustomDemoButtons extends PosComponent {
          setup() {
              super.setup();
            //   this.orm = useService("orm");
              useListener('click', this.onClick);
          }
          async onClick() {
            const { confirmed, payload } = await this.showPopup("TextInputPopup", {
                title: this.env._t('Enter Customer Reference'),
                body: this.env._t('Please enter the customer reference:'),
            });

                if (confirmed) {
                    localStorage.setItem('customerReference', payload);
                    
            }
        }
        
        
    }
    CustomDemoButtons.template = 'CustomDemoButtons';
      ProductScreen.addControlButton({
          component: CustomDemoButtons,
          condition: function() {
              return this.env.pos;
          },
      });
      Registries.Component.add(CustomDemoButtons);
      return CustomDemoButtons;
    });


odoo.define('bi_pos_product_toppings.PaymentScreen', function(require) {
    'use strict';
    const PaymentScreen = require('point_of_sale.PaymentScreen');
    const Registries = require('point_of_sale.Registries');
    const session = require('web.session');

    const InvoicePaymentScreen = PaymentScreen =>
        class extends PaymentScreen {
            setup() {
                super.setup();
            }

            async validateOrder(isForceValidate) {
                await super.validateOrder(isForceValidate);
                const order = this.env.pos.get_order();
                const orderId = order.uid;
                const customerReference = localStorage.getItem('customerReference');
                console.log("Order IDmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmm:",customerReference, orderId);
                const self = this;
               
                    this.rpc({
                        model: 'pos.order',
                        method: 'set_customer_reference',
                        args: [orderId, customerReference],
                    }).then(function(result) {
                        console.log("RPC result:", result);
                    }).guardedCatch(function(error) {
                        console.error("RPC error:", error);
                    });

                }
            }
      

    Registries.Component.extend(PaymentScreen, InvoicePaymentScreen);

    return PaymentScreen;
});
