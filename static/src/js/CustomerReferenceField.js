odoo.define('pos_button.Suggestion', function(require) {
    'use strict';

    const Order = require('point_of_sale.models').Order;
    const Registries = require('point_of_sale.Registries');

    const Suggestion = (Order) => class Suggestion extends Order {
        constructor(...args) {
            super(...args);
            this.customer_reference = this.customer_reference || null;
        }

        set_customer_reference(customer_reference) {
            this.customer_reference = customer_reference;
        }

        export_as_JSON() {
            const json = super.export_as_JSON(...arguments);
            json.customer_reference = this.customer_reference;
            return json;
        }

        init_from_JSON(json) {
            super.init_from_JSON(...arguments);
            this.customer_reference = json.customer_reference;
        }
    };

    Registries.Model.extend(Order, Suggestion);
});


odoo.define('pos_button.Custom', function(require) {
    'use strict';

    const PosComponent = require('point_of_sale.PosComponent');
    const { useListener } = require("@web/core/utils/hooks");
    const ProductScreen = require('point_of_sale.ProductScreen');
    const Registries = require('point_of_sale.Registries');

    class CustomDemoButtons extends PosComponent {
        setup() {
            super.setup();
            useListener('click', this.onClick);
        }
       
        async onClick() {
            const order = this.env.pos.get_order();
            const currentReference = order.customer_reference || '';
            console.log(currentReference,"pppppppppppppppppppppppppp")
            const { confirmed, payload } = await this.showPopup("TextInputPopup", {
                title: this.env._t('Enter Customer Reference'),
                body: this.env._t('Please enter the customer reference:'),
                value: currentReference,
            });

            if (confirmed) {
                const order = this.env.pos.get_order();
                order.set_customer_reference(payload); // Corrected reference to order
                console.log('Customer Reference Set:', order.customer_reference);
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
});
