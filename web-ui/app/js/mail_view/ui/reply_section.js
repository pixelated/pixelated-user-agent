define(
  [
    'flight/lib/component',
    'views/templates',
    'mail_view/ui/reply_box',
    'mail_view/ui/forward_box',
    'mixins/with_hide_and_show',
    'mixins/with_feature_toggle',
    'page/events'
  ],

  function (defineComponent, templates, ReplyBox, ForwardBox, withHideAndShow, withFeatureToggle, events) {
    'use strict';

    return defineComponent(replySection, withHideAndShow, withFeatureToggle('replySection'));

    function replySection() {
      this.defaultAttrs({
        replyButton: '#reply-button',
        replyAllButton: '#reply-all-button',
        forwardButton: '#forward-button',
        replyBox: '#reply-box',
        replyType: 'reply'
      });

      this.showReply = function() {
        this.attr.replyType = 'reply';
        this.fetchEmailToReplyTo();
      };

      this.showReplyAll = function() {
        this.attr.replyType = 'replyall';
        this.fetchEmailToReplyTo();
      };

      this.showForward = function() {
        this.attr.replyType = 'forward';
        this.fetchEmailToReplyTo();
      };

      this.render = function () {
        this.$node.html(templates.compose.replySection);

        this.on(this.select('replyButton'), 'click', this.showReply);
        this.on(this.select('replyAllButton'), 'click', this.showReplyAll);
        this.on(this.select('forwardButton'), 'click', this.showForward);
      };

      this.checkForDraftReply = function() {
        this.render();
        this.select('replyButton').hide();
        this.select('replyAllButton').hide();
        this.select('forwardButton').hide();

        this.trigger(document, events.mail.draftReply.want, {ident: this.attr.ident});
      };

      this.fetchEmailToReplyTo = function (ev) {
        this.trigger(document, events.mail.want, { mail: this.attr.ident, caller: this });
      };

      this.showDraftReply = function(ev, data) {
        this.hideButtons();
        ReplyBox.attachTo(this.select('replyBox'), { mail: data.mail, draftReply: true });
      };

      this.showReplyComposeBox = function (ev, data) {
        this.hideButtons();
        if(this.attr.replyType === 'forward') {
          ForwardBox.attachTo(this.select('replyBox'), { mail: data.mail });
        } else {
          ReplyBox.attachTo(this.select('replyBox'), { mail: data.mail, replyType: this.attr.replyType });
        }
      };

      this.hideButtons = function() {
        this.select('replyButton').hide();
        this.select('replyAllButton').hide();
        this.select('forwardButton').hide();
      };

      this.showButtons = function () {
        this.select('replyBox').empty();
        this.select('replyButton').show();
        this.select('replyAllButton').show();
        this.select('forwardButton').show();
      };

      this.after('initialize', function () {
        this.on(document, events.ui.replyBox.showReply, this.showReply);
        this.on(document, events.ui.replyBox.showReplyAll, this.showReplyAll);
        this.on(document, events.ui.composeBox.trashReply, this.showButtons);
        this.on(this, events.mail.here, this.showReplyComposeBox);
        this.on(document, events.dispatchers.rightPane.clear, this.teardown);

        this.on(document, events.mail.draftReply.notFound, this.showButtons);
        this.on(document, events.mail.draftReply.here, this.showDraftReply);

        this.checkForDraftReply();
      });
    }
  }
);
