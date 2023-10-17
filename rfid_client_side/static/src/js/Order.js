odoo.define('rfid_client_side.order', function (require) {
    const models = require('point_of_sale.models');
    let _super_Order = models.Order.prototype;
    models.Order = models.Order.extend({
        initialize: function (attributes, options) {
            _super_Order.initialize.apply(this, arguments);
            this.tags_info = [];
        },
//        export_for_printing: function () {
//            let result = _super_Order.export_for_printing.apply(this, arguments);
//            if(result){result['tags_info'] = this.tags_info;}
//        },
        set_tags_info: function (tags_info) {
            console.log("tags_info function",tags_info)
            this.tags_info = tags_info;
        },
        get_tags_info: function () {
            console.log("get_tags_info function")
            return this.tags_info;
        },

    });
});
