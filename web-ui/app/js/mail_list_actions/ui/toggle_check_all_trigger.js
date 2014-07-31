define(
  [
    'flight/lib/component',
    'page/events'
  ],

  function(defineComponent, events) {
    'use strict';

    return defineComponent(toggleCheckAllEmailsTrigger);

    function toggleCheckAllEmailsTrigger() {
      this.defaultAttrs({ });

      this.toggleCheckAll = function(event) {
        if (this.$node.prop('checked')) {
          this.trigger(document, events.ui.mails.checkAll);
        } else {
          this.trigger(document, events.ui.mails.uncheckAll);
        }
      };

      this.setCheckbox = function (event, state) {
        this.$node.prop('checked', state);
      };

      this.after('initialize', function () {
        this.on('click', this.toggleCheckAll);
        this.on(document, events.ui.mails.hasMailsChecked, this.setCheckbox);
      });
    }
  }
);
