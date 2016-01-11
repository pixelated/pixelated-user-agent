/*
 * Copyright (c) 2014 ThoughtWorks, Inc.
 *
 * Pixelated is free software: you can redistribute it and/or modify
 * it under the terms of the GNU Affero General Public License as published by
 * the Free Software Foundation, either version 3 of the License, or
 * (at your option) any later version.
 *
 * Pixelated is distributed in the hope that it will be useful,
 * but WITHOUT ANY WARRANTY; without even the implied warranty of
 * MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
 * GNU Affero General Public License for more details.
 *
 * You should have received a copy of the GNU Affero General Public License
 * along with Pixelated. If not, see <http://www.gnu.org/licenses/>.
 */
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
          .attachment(this.attr.attachments)
          .tag(tag);
      };

      this.renderDraftBox = function(ev, data) {
        var mail = data.mail;
        var body = mail.textPlainBody;
        this.attr.ident = mail.ident;
        this.render(templates.compose.box, {
          recipients: {
            to: mail.header.to,
            cc: mail.header.cc,
            bcc: mail.header.bcc
          },
          subject: mail.header.subject,
          body: body,
          attachments: mail.attachments
        });

        this.enableFloatlabel('input.floatlabel');
        this.enableFloatlabel('textarea.floatlabel');
        this.select('recipientsFields').show();
        this.select('bodyBox').focus();
        this.select('tipMsg').hide();
        this.enableAutoSave();
        this.bindCollapse();
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
        this.trigger(document, events.mail.want, { mail: this.attr.mailIdent , caller: this });
      });
    }
  }
);
