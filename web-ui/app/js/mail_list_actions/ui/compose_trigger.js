define(
  [
    'flight/lib/component',
    'views/templates',
    'page/events'
  ],

  function(defineComponent, templates, events) {
    'use strict';

    return defineComponent(composeTrigger);

    function composeTrigger() {

      this.defaultAttrs({});

      this.render = function() {
        this.$node.html(templates.mailActions.composeTrigger);
      };

      this.enableComposing = function(event, data) {
        this.trigger(document, events.dispatchers.rightPane.openComposeBox);
      };

      this.after('initialize', function () {
        this.render();
        this.on('click', this.enableComposing);
      });
    }
  }
);
