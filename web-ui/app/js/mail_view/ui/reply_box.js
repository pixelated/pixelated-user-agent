/*global Smail */
/*global _ */

define(
  [
    'flight/lib/component',
    'helpers/view_helper',
    'mixins/with_hide_and_show',
    'mixins/with_compose_inline',
    'page/events',
    'views/i18n'
  ],

  function (defineComponent, viewHelper, withHideAndShow, withComposeInline, events, i18n) {
    'use strict';

    return defineComponent(replyBox, withHideAndShow, withComposeInline);

    function replyBox() {
      this.defaultAttrs({
        replyType: 'reply',
        draftReply: false,
        mail: null,
        mailBeingRepliedIdent: undefined
      });

      this.getRecipients = function() {
        if (this.attr.replyType === 'replyall') {
          return this.attr.mail.replyToAllAddress();
        } else {
          return this.attr.mail.replyToAddress();
        }
      };

      var re = function(v) { return i18n('re') + v; };

      this.setupReplyBox = function() {
        var recipients, body;

        if (this.attr.draftReply){
          this.attr.ident = this.attr.mail.ident;
          this.attr.mailBeingRepliedIdent = this.attr.mail.draft_reply_for;

          recipients = this.attr.mail.recipients();
          body = this.attr.mail.body;
          this.attr.subject = this.attr.mail.header.subject;
        } else {
          this.attr.mailBeingRepliedIdent = this.attr.mail.ident;
          recipients = this.getRecipients();
          body = viewHelper.quoteMail(this.attr.mail);
          this.attr.subject = re(this.attr.mail.header.subject);
        }

        this.attr.recipientValues.to = recipients.to;
        this.attr.recipientValues.cc = recipients.cc;

        this.renderInlineCompose('reply-box', {
          recipients: recipients,
          subject: this.attr.subject,
          body: body
        });

        this.on(this.select('recipientsDisplay'), 'click keydown', this.showRecipientFields);
        this.on(this.select('subjectDisplay'), 'click', this.showSubjectInput);
      };

      this.showRecipientFields = function(ev, data) {
        if(!ev.keyCode || ev.keyCode === 13){
          this.select('recipientsDisplay').hide();
          this.select('recipientsFields').show();
          $('#recipients-to-area .tt-input').focus();
        }
      };

      this.showSubjectInput = function() {
        this.select('subjectDisplay').hide();
        this.select('subjectInput').show();
        this.select('subjectInput').focus();
      };

      this.buildMail = function(tag) {
        var builder = this.builtMail(tag).subject(this.select('subjectInput').val());
        if(!_.isUndefined(this.attr.mail.header.message_id)) {
          builder.header('in_reply_to', this.attr.mail.header.message_id);
        }

        if(!_.isUndefined(this.attr.mail.header.list_id)) {
          builder.header('list_id', this.attr.mail.header.list_id);
        }

        var mail = builder.build();
        mail.setDraftReplyFor(this.attr.mailBeingRepliedIdent);

        return mail;
      };

      this.after('initialize', function () {
        this.setupReplyBox();
      });
    }
  }
);
