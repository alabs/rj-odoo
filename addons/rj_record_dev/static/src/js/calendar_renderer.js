odoo.define('rj_record_dev.calendar_renderer', function (require) {
'use strict';

    var AbstractRenderer = require('web.AbstractRenderer');
    var config = require('web.config');
    var core = require('web.core');
    var Dialog = require('web.Dialog');
    var field_utils = require('web.field_utils');
    var FieldManagerMixin = require('web.FieldManagerMixin');
    var QWeb = require('web.QWeb');
    var relational_fields = require('web.relational_fields');
    var session = require('web.session');
    var utils = require('web.utils');
    var Widget = require('web.Widget');
    var CalendarRendererer = require('web.CalendarRenderer');

    var _t = core._t;
    var qweb = core.qweb;

    var CalendarRendererer_custom = CalendarRendererer.include({

       eventRender: function (event, element) {
            var $render = $(self._eventRender(event));
            event.title = $render.find('.o_field_type_char:first').text();
            element.find('.fc-content').html($render.html());
            element.addClass($render.attr('class'));
            if(event['record'].color){
                event.color_field = event['record'].color;
                element.css("background-color", event.color_field);
            }
            var display_hour = '';
            if (!event.allDay) {
                var start = event.r_start || event.start;
                var end = event.r_end || event.end;
                var timeFormat = _t.database.parameters.time_format.search("%H") != -1 ? 'HH:mm': 'h:mma';
                display_hour = start.format(timeFormat) + ' - ' + end.format(timeFormat);
                if (display_hour === '00:00 - 00:00') {
                    display_hour = _t('All day');
                }
            }
            element.find('.fc-content .fc-time').text(display_hour);
        },

    });
return CalendarRendererer_custom;
});

