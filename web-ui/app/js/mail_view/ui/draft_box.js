define(
  [
    'flight/lib/component',
    'views/templates',
    'mixins/with_mail_edit_base',
    'page/events',
    'mail_view/data/mail_builder'
  ],

  function (defineComponent, templates, withMailEditBase, events, mailBuilder) {
    'use strict';

    return defineComponent(draftBox, withMailEditBase);

    function draftBox() {
      this.defaultAttrs({
        closeMailButton: '.close-mail-button'
      });

      this.showNoMessageSelected = function() {
        this.trigger(events.dispatchers.rightPane.openNoMessageSelected);
      };

      this.buildMail = function(tag) {
        return this.builtMail(tag).build();
      };

      this.builtMail = function(tag) {
        return mailBuilder.newMail(this.attr.ident)
          .subject(this.select('subjectBox').val())
          .to(this.attr.recipientValues.to)
          .cc(this.attr.recipientValues.cc)
          .bcc(this.attr.recipientValues.bcc)
          .body(this.select('bodyBox').val())
          .tag(tag);
      };

      this.renderDraftBox = function(ev, data) {
        var mail = data.mail;
        this.attr.ident = mail.ident;

        this.render(templates.compose.box, {
          recipients: {
            to: mail.header.to,
            cc: mail.header.cc,
            bcc: mail.header.bcc
          },
          subject: mail.header.subject,
          body: mail.body
        });

        this.select('recipientsFields').show();
        this.select('bodyBox').focus();
        this.select('tipMsg').hide();
        this.enableAutoSave();
        this.on(this.select('cancelButton'), 'click', this.showNoMessageSelected);
        this.on(this.select('closeMailButton'), 'click', this.showNoMessageSelected);
      };

      this.mailDeleted = function(event, data) {
        if (_.contains(_.pluck(data.mails, 'ident'),  this.attr.ident)) {
          this.trigger(events.dispatchers.rightPane.openNoMessageSelected);
        }
      };

      this.after('initialize', function () {
        this.on(this, events.mail.here, this.renderDraftBox);
        this.on(document, events.mail.sent, this.showNoMessageSelected);
        this.on(document, events.mail.deleted, this.mailDeleted);
        this.trigger(document, events.mail.want, { mail: this.attr.mailIdent, caller: this });
      });
    }
  }
);
