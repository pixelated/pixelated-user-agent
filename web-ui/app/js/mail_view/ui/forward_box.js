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
    'helpers/view_helper',
    'mixins/with_hide_and_show',
    'mixins/with_compose_inline',
    'page/events',
    'views/i18n'
  ],

  function (defineComponent, viewHelper, withHideAndShow, withComposeInline, events, i18n) {
    'use strict';

    return defineComponent(forwardBox, withHideAndShow, withComposeInline);

    function forwardBox() {
      var fwd = function(v) { return i18n('Fwd: ') + v; };

      this.fetchTargetMail = function (ev) {
        this.trigger(document, events.mail.want, { mail: this.attr.ident, caller: this });
      };

      this.setupForwardBox = function() {
        var mail = this.attr.mail;
        this.attr.subject = fwd(mail.header.subject);
        this.attr.attachments = mail.attachments;

        this.renderInlineCompose('forward-box', {
          subject: this.attr.subject,
          recipients: { to: [], cc: []},
          body: viewHelper.quoteMail(mail),
          attachments: this.convertToRemovableAttachments(mail.attachments)
        });

        var self = this;
        this.$node.find('i.remove-icon').bind('click', function(event) {
          var element = $(this);
          var ident = element.closest('li').attr('data-ident');
          self.trigger(document, events.mail.removeAttachment, {ident: ident});
          event.preventDefault();
        });
        
        this.on(this.select('subjectDisplay'), 'click', this.showSubjectInput);
        this.select('recipientsDisplay').hide();
        this.select('recipientsFields').show();
      };

      this.convertToRemovableAttachments = function(attachments) {
        return attachments.map(function(attachment) {
          attachment.removable = true;
          return attachment;
        });
      };

      this.showSubjectInput = function() {
        this.select('subjectDisplay').hide();
        this.select('subjectInput').show();
        this.select('subjectInput').focus();
      };

      this.buildMail = function(tag) {
        var builder = this.builtMail(tag).subject(this.select('subjectInput').val());

        var headersToFwd = ['bcc', 'cc', 'date', 'from', 'message_id', 'reply_to', 'sender', 'to'];
        var header = this.attr.mail.header;
        _.each(headersToFwd, function (h) {
          if (!_.isUndefined(header[h])) {
            builder.header('resent_' + h, header[h]);
          }
        });

        return builder.build();
      };

      this.after('initialize', function () {
        this.setupForwardBox();
      });
    }
  }
);
