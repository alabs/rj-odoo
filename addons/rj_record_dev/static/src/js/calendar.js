odoo.define('rj_record_dev.calendar', function (require) {
'use strict';

    var AbstractModel = require('web.AbstractModel');
    var Context = require('web.Context');
    var core = require('web.core');
    var fieldUtils = require('web.field_utils');
    var session = require('web.session');
    var Calendar = require('web.CalendarModel');

    var QWeb = core.qweb;
    var _t = core._t;

    var Calendar_custom = Calendar.include({

       _recordToCalendarEvent: function (evt) {
            var res = this._super.apply(this, arguments);
            var color_key = evt[this.fieldColor];
            res['color_field'] = "";
            return res;
        },

    });
return Calendar_custom;
});

