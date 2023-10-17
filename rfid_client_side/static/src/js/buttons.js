odoo.define('rfid_client_side.rfid_sales_button', function (require) {
    'use strict';

    const PosComponent = require('point_of_sale.PosComponent');
    const ProductScreen = require('point_of_sale.ProductScreen');
    const {useListener} = require('web.custom_hooks');
    const Registries = require('point_of_sale.Registries');
    const ajax = require('web.ajax');
    var rpc = require('web.rpc');

    class rfid_sales_button extends PosComponent {
        constructor() {
            super(...arguments);
            useListener('click', this.onClick);
        }

        get isHighlighted() {
            return true
        }

        async onClick() {
            var loader_icon = $(".se-pre-con");
            var please_wait = $(".se-pre-con p ");
            loader_icon.css({
                 "display": "block",
                 "border": "none",
                 "position": "fixed",
                 "left": "0px",
                 "top": "-15%",
                 "width": "100%",
                 "height": "100%",
                 "z-index": "9999",
                 "background": "url(/rfid_client_side/static/src/img/Preloader_11.gif) center no-repeat",
            });
            please_wait.removeClass('oe_hidden');
            var products = false;
            var serials = false;
            var self = this;
            var order = this.env.pos.get_order();
            var server_side_url = false;
            if(!order){
                order = new models.Order({}, {pos: this.env.pos});
            }
            var successful = await rpc.query({
                model: 'ir.config_parameter',
                method: 'get_param',
                args: ["server_side_url"],
            }).then(function(param) {
                server_side_url = param
                return true;
            });
            if(successful){
                var promise = await ajax.jsonRpc("/api/rfid_get_serials_pos", 'call', {
                    'DeviceSerialNumberSale': this.env.pos.config.DeviceSerialNumberSale,
                    'server_side_url': server_side_url,
                    'sales': true,
                }).then(function(res) {
                    if(res['serials']){
                        serials = res['serials'];
                        return true;
                    }
                    return false;
                });
                if(promise){
                    if(serials.length != 0){
                        var promise2 = await ajax.jsonRpc("/api/rfid_get_products_pos", 'call', {
                            'serials': serials,
                            'session_id': order.session_id || false,
                            'sales' : true,
                        }).then(function(res) {
                            if(res['products']){
                                products = res['products'];
                                return true;
                            }
                            return false;
                        });
                        if(promise2){
                            if(products.length != 0){
                                for (var i = 0; i < products.length; i++) {
//                                    console.log("products[i]['product_id']",products[i]['product_id']);
                                    var product = this.env.pos.db.get_product_by_id(products[i]['product_id']);
                                    var modifiedPackLotLines = {}
                                    var newPackLotLines =products[i]['EPC'];
                                    var draftPackLotLines = { modifiedPackLotLines, newPackLotLines };
                                    order.add_product(product, {
                                        draftPackLotLines: draftPackLotLines,
                                    });

                                }
                                order.set_tags_info(products);
                                loader_icon.css({"z-index": "-1"});
                                please_wait.addClass('oe_hidden');
                            }
                            else{loader_icon.css({"z-index": "-1"});please_wait.addClass('oe_hidden');alert("There Are No Sales Yet!")}

                       }
                    }
                    else{loader_icon.css({"z-index": "-1"});please_wait.addClass('oe_hidden');alert("There Are No Sales Yet!")}

                }
                else{loader_icon.css({"z-index": "-1"});please_wait.addClass('oe_hidden');alert("There Are No Sales Yet!")}
            }
        }
    }

    rfid_sales_button.template = 'rfid_sales_button';

    ProductScreen.addControlButton({
        component: rfid_sales_button,
        condition: function () {
            return true;
        },
    });

    Registries.Component.add(rfid_sales_button);

    class rfid_return_button extends PosComponent {
        constructor() {
            super(...arguments);
            useListener('click', this.onClick);
        }

        get isHighlighted() {
            return true
        }

        async onClick() {
            var loader_icon = $(".se-pre-con");
            var please_wait = $(".se-pre-con p ");
            loader_icon.css({
                 "display": "block",
                 "border": "none",
                 "position": "fixed",
                 "left": "0px",
                 "top": "-15%",
                 "width": "100%",
                 "height": "100%",
                 "z-index": "9999",
                 "background": "url(/rfid_client_side/static/src/img/Preloader_11.gif) center no-repeat",
            });
            please_wait.removeClass('oe_hidden');
            var products = false;
            var serials = false;
            var self = this;
            var order = this.env.pos.get_order();
            var server_side_url = false;
            if(!order){
                order = new models.Order({}, {pos: this.env.pos});
            }
            var successful = await rpc.query({
                model: 'ir.config_parameter',
                method: 'get_param',
                args: ["server_side_url"],
            }).then(function(param) {
                server_side_url = param
                return true;
            });
            if(successful){
                var promise = await ajax.jsonRpc("/api/rfid_get_serials_pos", 'call', {
                    'DeviceSerialNumberSale': this.env.pos.config.DeviceSerialNumberReturn,
                    'server_side_url': server_side_url,
                    'returns': true,
                }).then(function(res) {
                    if(res['serials']){
                        serials = res['serials'];
                        return true;
                    }
                    return false;
                });
                if(promise){
                    if(serials.length != 0){
                        var promise2 = await ajax.jsonRpc("/api/rfid_get_products_pos", 'call', {
                            'serials': serials,
                            'session_id': order.session_id || false,
                            'returns' : true,
                        }).then(function(res) {
                            if(res['products']){
                                products = res['products'];
                                return true;
                            }
                            return false;
                        });
                        if(promise2){
                            if(products.length != 0){
                                for (var i = 0; i < products.length; i++) {
                                    var product = this.env.pos.db.get_product_by_id(products[i]['product_id']);
                                    var modifiedPackLotLines = {}
                                    var newPackLotLines =products[i]['EPC'];
                                    var draftPackLotLines = { modifiedPackLotLines, newPackLotLines };
                                    order.add_product(product, {
                                        draftPackLotLines : draftPackLotLines,
                                        quantity: -1,
                                    });
                                }
                                order.set_tags_info(products);
                                loader_icon.css({"z-index": "-1"});
                                please_wait.addClass('oe_hidden');
                            }
                            else{loader_icon.css({"z-index": "-1"});alert("There Are No Returns Yet!")}

                       }
                    }
                    else{loader_icon.css({"z-index": "-1"});alert("There Are No Returns Yet!")}

                }
                else{loader_icon.css({"z-index": "-1"});alert("There Are No Returns Yet!")}
            }
        }
    }

    rfid_return_button.template = 'rfid_return_button';

    ProductScreen.addControlButton({
        component: rfid_return_button,
        condition: function () {
            return true;
        },
    });

    Registries.Component.add(rfid_return_button);

//    return rfid_return_button;
});
