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
/*global _ */

define(
  [
    'page/events',
    'views/templates',
    'mail_view/data/mail_builder',
    'mixins/with_mail_edit_base'
  ],
  function(events, templates, mailBuilder, withMailEditBase) {
    'use strict';

    function withComposeInline() {
      this.defaultAttrs({
        subjectDisplay: '#reply-subject',
        subjectInput: '#subject-container input',
        recipientsDisplay: '#all-recipients'
      });

      this.openMail = function(ev, data) {
        this.trigger(document, events.ui.mail.open, {ident: this.attr.mail.ident});
      };

      this.trashReply = function() {
        this.trigger(document, events.ui.composeBox.trashReply);
        this.teardown();
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

      this.renderInlineCompose = function(className, viewData) {
        this.show();
        this.render(templates.compose.inlineBox, viewData);

        this.$node.addClass(className);
        this.select('bodyBox').focus();

        this.enableAutoSave();
      };

      this.updateIdent = function(ev, data) {
        this.attr.mail.ident = data.ident;
      };

      this.after('initialize', function () {
        this.on(document, events.mail.sent, this.openMail);
        this.on(document, events.mail.deleted, this.trashReply);
        this.on(document, events.mail.draftSaved, this.updateIdent);
      });

      withMailEditBase.call(this);
    }

    return withComposeInline;
  });
