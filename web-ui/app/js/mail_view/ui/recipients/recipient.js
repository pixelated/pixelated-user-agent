'use strict';

define(
  [
    'flight/lib/component',
    'views/templates'
  ],

  function (defineComponent, templates) {

    return defineComponent(recipient);

    function recipient() {
      this.renderAndPrepend = function (nodeToPrependTo, recipient) {
        var html = $(templates.compose.fixedRecipient(recipient));
        html.insertBefore(nodeToPrependTo.children().last());
        var component = new this.constructor();
        component.initialize(html, recipient);
        return component;
      };

      this.destroy = function () {
        this.$node.remove();
        this.teardown();
      };

      this.select = function () {
        this.$node.find('.recipient-value').addClass('selected');
      };

      this.unselect = function () {
        this.$node.find('.recipient-value').removeClass('selected');
      };
    }
  }
);
