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
        _eventRender: function (event) {
            var qweb_context = {
                event: event,
                fields: this.state.fields,
                format: this._format.bind(this),
                isMobile: config.device.isMobile,
                read_only_mode: this.read_only_mode,
                record: event.record,
                user_context: session.user_context,
                widget: this,
            };
            this.qweb_context = qweb_context;
            if (_.isEmpty(qweb_context.record)) {
                return '';
            } else {
                return (this.qweb || qweb).render("calendar-box", qweb_context);
            }
        },

    _initCalendar: function () {
        var self = this;

        this.$calendar = this.$(".o_calendar_widget");

        // This seems like a workaround but apparently passing the locale
        // in the options is not enough. We should initialize it beforehand
        var locale = moment.locale();
        $.fullCalendar.locale(locale);

        //Documentation here : http://arshaw.com/fullcalendar/docs/
        var fc_options = $.extend({}, this.state.fc_options, {
            eventDrop: function (event) {
                self.trigger_up('dropRecord', event);
            },
            eventResize: function (event) {
                self.trigger_up('updateRecord', event);
            },
            eventClick: function (event) {
                self.trigger_up('openEvent', event);
                self.$calendar.fullCalendar('unselect');
            },
            select: function (target_date, end_date, event, _js_event, _view) {
                var data = {'start': target_date, 'end': end_date};
                if (self.state.context.default_name) {
                    data.title = self.state.context.default_name;
                }
                self.trigger_up('openCreate', data);
                self.$calendar.fullCalendar('unselect');
            },
            eventRender: function (event, element) {
                var $render = $(self._eventRender(event));
                event.title = $render.find('.o_field_type_char:first').text();
                element.find('.fc-content').html($render.html());
                element.addClass($render.attr('class'));
//                if(event['record'].color){
//                    event.color_field = event['record'].color;
//                    element.css("background-color", event.color_field);
//                }
                if(event['record'].calen_tag == 'CRITICO'){
                    element.css("background-color", 'Red');
                    element.css("color", 'white');
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
//            eventRender: function (event, element) {
//                var $render = $(self._eventRender(event));
//                event.title = $render.find('.o_field_type_char:first').text();
//                element.find('.fc-content').html($render.html());
//                element.addClass($render.attr('class'));
//                var display_hour = '';
//                if (!event.allDay) {
//                    var start = event.r_start || event.start;
//                    var end = event.r_end || event.end;
//                    var timeFormat = _t.database.parameters.time_format.search("%H") != -1 ? 'HH:mm': 'h:mma';
//                    display_hour = start.format(timeFormat) + ' - ' + end.format(timeFormat);
//                    if (display_hour === '00:00 - 00:00') {
//                        display_hour = _t('All day');
//                    }
//                }
//                element.find('.fc-content .fc-time').text(display_hour);
//            },
            // Dirty hack to ensure a correct first render
            eventAfterAllRender: function () {
                $(window).trigger('resize');
            },
            viewRender: function (view) {
                // compute mode from view.name which is either 'month', 'agendaWeek' or 'agendaDay'
                var mode = view.name === 'month' ? 'month' : (view.name === 'agendaWeek' ? 'week' : 'day');
                self.trigger_up('viewUpdated', {
                    mode: mode,
                    title: view.title,
                });
            },
            height: 'parent',
            unselectAuto: false,
            isRTL: _t.database.parameters.direction === "rtl",
            locale: locale, // reset locale when fullcalendar has already been instanciated before now
        });

        this.$calendar.fullCalendar(fc_options);
    },


    });
return CalendarRendererer_custom;
});

