odoo.define('rfid_client_side.PaymentScreen', function (require) {
    'use strict';

    const PaymentScreen = require('point_of_sale.PaymentScreen');
    const Registries = require('point_of_sale.Registries');
    const core = require('web.core');
    const _t = core._t;
    const ajax = require('web.ajax');
    var rpc = require('web.rpc');

    const RfidPaymentScreen = (PaymentScreen) =>
        class extends PaymentScreen {
            async validateOrder(isForceValidate) {
                  var server_side_url = false;
                  var successful = await rpc.query({
                        model: 'ir.config_parameter',
                        method: 'get_param',
                        args: ["server_side_url"],
                  }).then(function(param) {
                        server_side_url = param
                        return true;
                  });
                  if(successful){
                      var order = this.env.pos.get_order();
                      var orderline =  order.get_orderlines();
                      var tags = order.get_tags_info();
//                      console.log("tags",tags);
                      var tags_to_remove = [];
                      for (var i = 0; i < orderline.length; i++) {
                          for (var ii = 0; ii < tags.length; ii++) {
                             if(orderline[i].get_product().id == tags[ii]['product_id']){
                                tags_to_remove.push({
                                    tag_id: tags[ii]['tag_id'],
                                });
                             }
                          }
                      }
                      if(tags_to_remove){
                        var promise = await ajax.jsonRpc("/api/remove_tags_info_clientside", 'call', {'tags': tags_to_remove,'server_side_url':server_side_url})
                      }
//                      console.log("tags_to_remove",tags_to_remove);
                  }
                  await super.validateOrder(isForceValidate);
            }
        }
    Registries.Component.extend(PaymentScreen, RfidPaymentScreen);

    return RfidPaymentScreen;
});
