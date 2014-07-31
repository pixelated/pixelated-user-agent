define(
  [
    'flight/lib/component',
    'page/events'
  ],

  function (defineComponent, events) {
    'use strict';

    return defineComponent(draftSaveStatus);

    function draftSaveStatus() {
      this.setMessage = function(msg) {
        var node = this.$node;
        return function () { node.text(msg); };
      };

      this.after('initialize', function () {
        this.on(document, events.mail.saveDraft, this.setMessage('Saving to Drafts...'));
        this.on(document, events.mail.draftSaved, this.setMessage('Draft Saved.'));
        this.on(document, events.ui.mail.changedSinceLastSave, this.setMessage(''));
      });
    }
  }
);
