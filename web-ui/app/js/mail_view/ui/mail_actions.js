/*global Smail */
/*global _ */

define(
  [
    'flight/lib/component',
    'views/templates',
    'page/events'
  ],

  function (defineComponent, templates, events) {
    'use strict';

    return defineComponent(mailActions);

    function mailActions() {

      this.defaultAttrs({
        replyButtonTop: '#reply-button-top',
        viewMoreActions: '#view-more-actions',
        replyAllButtonTop: '#reply-all-button-top',
        deleteButtonTop: '#delete-button-top',
        moreActions: '#more-actions'
      });


      this.displayMailActions = function () {

        this.$node.html(templates.mails.mailActions());

        this.select('moreActions').hide();

        this.on(this.select('replyButtonTop'), 'click', function () {
          this.trigger(document, events.ui.replyBox.showReply);
        }.bind(this));

        this.on(this.select('replyAllButtonTop'), 'click', function () {
          this.trigger(document, events.ui.replyBox.showReplyAll);
          this.select('moreActions').hide();
        }.bind(this));

        this.on(this.select('deleteButtonTop'), 'click', function () {
          this.trigger(document, events.ui.mail.delete, {mail: this.attr.mail});
          this.select('moreActions').hide();
        }.bind(this));

        this.on(this.select('viewMoreActions'), 'click', function () {
          this.select('moreActions').toggle();
        }.bind(this));

        this.on(this.select('viewMoreActions'), 'blur', function (event) {
          var replyButtonTopHover = this.select('replyAllButtonTop').is(':hover');
          var deleteButtonTopHover = this.select('deleteButtonTop').is(':hover');

          if (replyButtonTopHover || deleteButtonTopHover) {
            event.preventDefault();
          } else {
            this.select('moreActions').hide();
          }
        }.bind(this));

      };

      this.after('initialize', function () {
        this.on(document, events.dispatchers.rightPane.clear, this.teardown);
        this.displayMailActions();
      });
    }
  }
);
