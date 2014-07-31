define(
  [
    'flight/lib/component',
    'views/templates',
    'mixins/with_hide_and_show',
    'page/events'
  ],

  function(defineComponent, templates, withHideAndShow, events) {
    'use strict';

    return defineComponent(userAlerts, withHideAndShow);

    function userAlerts() {
      this.defaultAttrs({
        dismissTimeout: 3000
      });

      this.render = function (message) {
        this.$node.html(templates.userAlerts.message(message));
        this.show();
        setTimeout(this.hide.bind(this), this.attr.dismissTimeout);
      };


      this.displayMessage = function (ev, data) {
        this.render({ message: data.message});
      };

      this.after('initialize', function () {
        this.on(document, events.ui.userAlerts.displayMessage, this.displayMessage);
      });
    }
  }
);
