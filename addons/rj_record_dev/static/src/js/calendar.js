odoo.define('rj_record_dev.calendar', function (require) {
'use strict';

var Calendar = require('web.CalendarModel');

var QWeb = core.qweb;
var _t = core._t;
Calendar.include({

    _recordToCalendarEvent : function (evt) {
            var res = this._super.apply(this, arguments);
            var color_key = evt[this.fieldColor];
            return res;
        }
});
});

