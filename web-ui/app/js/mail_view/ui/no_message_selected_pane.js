define(
  [
    'flight/lib/component',
    'views/templates',
    'mixins/with_hide_and_show',
    'page/events'
  ],

  function(defineComponent, templates, withHideAndShow, events) {
    'use strict';

    return defineComponent(noMessageSelectedPane, withHideAndShow);

    function noMessageSelectedPane() {
      this.render = function() {
        this.$node.html(templates.noMessageSelected());
      };

      this.after('initialize', function () {
        this.render();
        this.on(document, events.dispatchers.rightPane.clear, this.teardown);
      });
    }
  }
);
