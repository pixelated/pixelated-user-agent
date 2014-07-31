define(
  [
    'flight/lib/component',
    'views/templates',
    'mixins/with_enable_disable_on_event',
    'page/events'
  ],

  function(defineComponent, templates, withEnableDisableOnEvent, events) {
    'use strict';

    return defineComponent(deleteManyTrigger, withEnableDisableOnEvent(events.ui.mails.hasMailsChecked));

    function deleteManyTrigger() {
      this.defaultAttrs({});

      this.getMailsToDelete = function(event) {
        this.trigger(document, events.ui.mail.wantChecked, this.$node);
      };

      this.deleteManyEmails = function (event, data) {
        this.trigger(document, events.ui.mail.deleteMany, data);
      };

      this.after('initialize', function () {
        this.on('click', this.getMailsToDelete);
        this.on(events.ui.mail.hereChecked, this.deleteManyEmails);
      });
    }
  }
);
