define(
  [
    'flight/lib/component',
    'views/templates',
    'mixins/with_enable_disable_on_event',
    'page/events'
  ],

  function(defineComponent, templates, withEnableDisableOnEvent, events) {
    'use strict';

    return defineComponent(markAsUnreadTrigger, withEnableDisableOnEvent(events.ui.mails.hasMailsChecked));

    function markAsUnreadTrigger() {
      this.defaultAttrs({});

      this.getMailsToMarkAsUnread = function(event) {
        this.trigger(document, events.ui.mail.wantChecked, this.$node);
      };

      this.markManyEmailsAsUnread = function (event, data) {
        this.trigger(document, events.mail.unread, data);
      };

      this.after('initialize', function () {
        this.on('click', this.getMailsToMarkAsUnread);
        this.on(events.ui.mail.hereChecked, this.markManyEmailsAsUnread);
      });
    }
  }
);
