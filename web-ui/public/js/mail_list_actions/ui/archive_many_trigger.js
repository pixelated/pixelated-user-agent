define(
  [
    'flight/lib/component',
    'views/templates',
    'mixins/with_enable_disable_on_event',
    'page/events'
  ],

  function(definecomponent, templates, withEnableDisableOnEvent, events) {
    'use strict';

    return definecomponent(archiveManyTrigger, withEnableDisableOnEvent(events.ui.mails.hasMailsChecked));
    function archiveManyTrigger() {

      this.getMailsToArchive = function() {
        this.trigger(document, events.ui.mail.wantChecked, this.$node);
      };

      this.archiveManyEmails = function(event, data) {
        this.trigger(document, events.mail.archiveMany, data);
      };

      this.after('initialize', function () {
        this.on('click', this.getMailsToArchive);
        this.on(events.ui.mail.hereChecked, this.archiveManyEmails);
      });
    }
  }
);
