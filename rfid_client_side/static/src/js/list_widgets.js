/* Add one more option to boolean_button form widget (displayed in the product.template form view) */
odoo.define('rfid_client_side.list_widgets', function (require) {
"use strict";

  var core = require('web.core');
  var ListController = require('web.ListController');
  var FormController = require('web.FormController');
  var _t = core._t;

  ListController.include({
    renderButtons: function ($node) {
      var self = this;
      this._super.apply(this, arguments); // Sets this.$buttons
      if(self.modelName == 'stock.inventory.line') {
        this.$buttons.find('.o_list_button_add_custom').css('display', 'inline')
        this.$buttons.on('click', '.o_list_button_add_custom', function(ev) {
          ev.preventDefault();
            self._rpc({
                fields: ['name','id',],
                model: 'stock.inventory',
                method: 'update_orderline_state',
                args: [self.inventory_id],
            }).then(function (result) {
            });
        });
      };
      if(self.modelName == 'stock.inventory.line') {
        this.$buttons.find('.o_list_button_add_custom_delete').css('display', 'inline')
        this.$buttons.on('click', '.o_list_button_add_custom_delete', function(ev) {
          ev.preventDefault();
            self._rpc({
                fields: ['name','id',],
                model: 'stock.inventory',
                method: 'delete_date',
                args: [self.inventory_id],
            }).then(function (result) {
            });
        });
      };
      if(self.modelName == 'stock.inventory.line') {
        this.$buttons.find('.o_list_button_add_custom1').css('display', 'inline')
        this.$buttons.on('click', '.o_list_button_add_custom1', function(ev) {
          ev.preventDefault();
            self._rpc({
                fields: ['name','id',],
                model: 'stock.inventory',
                method: 'get_adjustments',
                args: [self.inventory_id],
            }).then(function (result) {
            });
        });
      }
    },
  });

//  ListController.include({
//    renderButtons: function ($node) {
//      var self = this;
//      this._super.apply(this, arguments); // Sets this.$buttons
//      if(self.modelName == 'stock.inventory.line') {
//        this.$buttons.find('.o_list_button_add_custom1').css('display', 'inline')
//        this.$buttons.on('click', '.o_list_button_add_custom1', function(ev) {
//          ev.preventDefault();
//            self._rpc({
//                fields: ['name','id',],
//                model: 'stock.inventory',
//                method: 'get_adjustments',
//                args: [self.inventory_id],
//            }).then(function (result) {
//            });
//        });
//      }
//    },
//  });

});

