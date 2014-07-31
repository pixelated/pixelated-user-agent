define(
  [
    'flight/lib/component',
    'views/templates',
    'page/events'
  ],

  function(defineComponent, templates, events) {
    'use strict';

    return defineComponent(refreshTrigger);

    function refreshTrigger() {
      this.render = function() {
        this.$node.html(templates.mailActions.refreshTrigger);
      };

      this.refresh = function(event) {
        this.trigger(document, events.ui.mails.refresh);
      };

      this.after('initialize', function () {
        this.render();
        this.on('click', this.refresh);
      });
    }
  }
);
