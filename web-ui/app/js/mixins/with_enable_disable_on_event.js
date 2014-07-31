/*global Smail */
/*global _ */

define([],
  function () {
    'use strict';

    function withEnableDisableOnEvent(ev) {
      return function () {
        this.disableElement = function () {
          this.$node.attr('disabled', 'disabled');
        };

        this.enableElement = function () {
          this.$node.removeAttr('disabled');
        };

        this.toggleEnabled = function (ev, enable) {
          if (enable) {
            this.enableElement();
          } else {
            this.disableElement();
          }
        };

        this.after('initialize', function () {
          this.on(document, ev, this.toggleEnabled);
        });
      };
    }

    return withEnableDisableOnEvent;
  }
);
