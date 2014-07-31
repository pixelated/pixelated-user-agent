define(
  [
    'flight/lib/component',
    'views/templates',
    'mixins/with_enable_disable_on_event',
    'page/events'
  ],

  function(defineComponent, templates, withEnableDisableOnEvent, events) {
    'use strict';

    return defineComponent(markManyAsReadTrigger, withEnableDisableOnEvent(events.ui.mails.hasMailsChecked));

    function markManyAsReadTrigger() {
      this.defaultAttrs({});

      this.getMailsToMarkAsRead = function(event) {
        this.trigger(document, events.ui.mail.wantChecked, this.$node);
      };

      this.markManyEmailsAsRead = function (event, data) {
        this.trigger(document, events.mail.read, data);
      };

      this.after('initialize', function () {
        this.on('click', this.getMailsToMarkAsRead);
        this.on(events.ui.mail.hereChecked, this.markManyEmailsAsRead);
      });
    }
  }
);
