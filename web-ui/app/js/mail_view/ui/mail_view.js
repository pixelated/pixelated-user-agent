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
    'mail_view/ui/mail_actions',
    'helpers/view_helper',
    'mixins/with_hide_and_show',
    'mixins/with_mail_tagging',
    'page/events',
    'views/i18n'
  ],

  function (defineComponent, templates, mailActions, viewHelpers, withHideAndShow, withMailTagging, events, i18n) {
  'use strict';

    return defineComponent(mailView, mailActions, withHideAndShow, withMailTagging);

    function mailView() {
      this.defaultAttrs({
        tags: '.tag',
        newTagInput: '#new-tag-input',
        newTagButton: '#new-tag-button',
        addNew: '.add-new',
        trashButton: '#trash-button',
        archiveButton: '#archive-button',
        closeMailButton: '.close-mail-button'
      });

      this.displayMail = function (event, data) {
        this.attr.mail = data.mail;

        var signed, encrypted, attachments;

        data.mail.security_casing = data.mail.security_casing || {};
        signed = this.checkSigned(data.mail);
        encrypted = this.checkEncrypted(data.mail);
        attachments = data.mail.attachments.map(function (attachment) {
            attachment.received = true;
            return attachment;
        });

        if(data.mail.mailbox === 'sent') {
          encrypted = undefined;
        }

        this.$node.html(templates.mails.fullView({
          header: data.mail.header,
          body: [],
          statuses: viewHelpers.formatStatusClasses(data.mail.status),
          ident: data.mail.ident,
          tags: data.mail.tags,
          encryptionStatus: encrypted,
          signatureStatus: signed,
          attachments: attachments
        }));

        this.$node.find('.bodyArea').html(viewHelpers.formatMailBody(data.mail));

        this.trigger(document, events.search.highlightResults, {where: '.bodyArea'});
        this.trigger(document, events.search.highlightResults, {where: '.subjectArea'});
        this.trigger(document, events.search.highlightResults, {where: '.msg-header .recipients'});
        this.trigger(document, events.ui.replyBox.showReplyContainer);

        this.attachTagCompletion(this.attr.mail);

        this.select('tags').on('click', function (event) {
          this.removeTag($(event.target).text());
        }.bind(this));

        this.addTagLoseFocus();
        this.on(this.select('newTagButton'), 'click', this.showNewTagInput);
        this.on(this.select('newTagInput'), 'keydown', this.handleKeyDown);
        this.on(this.select('newTagInput'), 'blur', this.addTagLoseFocus);
        this.on(this.select('trashButton'), 'click', this.moveToTrash);
        this.on(this.select('closeMailButton'), 'click', this.openNoMessageSelectedPane);

        mailActions.attachTo('#mail-actions', data);
        this.resetScroll();
      };

      this.resetScroll = function(){
        $('#right-pane').scrollTop(0);
      };

      this.checkEncrypted = function(mail) {
        if(_.isEmpty(mail.security_casing.locks)) { return 'not-encrypted'; }

        var status = ['encrypted'];

        var hasAnyEncryptionInfo = _.any(mail.security_casing.locks, function (lock) {
          return lock.state === 'valid';
        });

        if(hasAnyEncryptionInfo) {
          status.push('encryption-valid');
        } else {
          status.push('encryption-error');
        }

        return status.join(' ');
      };

      this.checkSigned = function(mail) {
        if(_.isEmpty(mail.security_casing.imprints)) {
          return 'not-signed';
        }

        var hasNoSignatureInformation = _.any(mail.security_casing.imprints, function (imprint) {
          return imprint.state === 'no_signature_information';
        });

        if(hasNoSignatureInformation) {
          return 'not-signed';
        }

        var status = ['signed'];

        if(_.any(mail.security_casing.imprints, function(imprint) { return imprint.state === 'from_revoked'; })) {
          status.push('signature-revoked');
        }
        if(_.any(mail.security_casing.imprints, function(imprint) { return imprint.state === 'from_expired'; })) {
          status.push('signature-expired');
        }

        if(this.isNotTrusted(mail)) {
          status.push('signature-not-trusted');
        }

        return status.join(' ');
      };

      this.isNotTrusted = function(mail){
        return _.any(mail.security_casing.imprints, function(imprint) {
          if(_.isNull(imprint.seal)){
            return true;
          }
          var currentTrust = _.isUndefined(imprint.seal.trust) ? imprint.seal.validity : imprint.seal.trust;
          return currentTrust === 'no_trust';
        });
      };

      this.openNoMessageSelectedPane = function(ev, data) {
        this.trigger(document, events.dispatchers.rightPane.openNoMessageSelected);
      };

      this.handleKeyDown = function(event) {
        var ENTER_KEY = 13;
        var ESC_KEY = 27;

        if (event.which === ENTER_KEY){
          event.preventDefault();
          if (this.select('newTagInput').val().trim() !== '') {
            this.createNewTag();
          }
        } else if (event.which === ESC_KEY) {
          event.preventDefault();
          this.addTagLoseFocus();
        }
      };

      this.addTagLoseFocus = function () {
        this.select('newTagInput').hide();
        this.select('newTagInput').typeahead('val', '');
        this.select('addNew').show();
      };

      this.showNewTagInput = function () {
        this.select('newTagInput').show();
        this.select('newTagInput').focus();
        this.select('addNew').hide();
      };

      this.removeTag = function (tag) {
        tag = tag.toString();
        var filteredTags = _.without(this.attr.mail.tags, tag);
        this.updateTags(this.attr.mail, filteredTags);
        this.trigger(document, events.dispatchers.tags.refreshTagList);
      };

      this.moveToTrash = function(){
        this.trigger(document, events.ui.mail.delete, { mail: this.attr.mail });
      };

      this.tagsUpdated = function(ev, data) {
        data = data || {};
        this.attr.mail.tags = data.tags;
        this.displayMail({}, { mail: this.attr.mail });
      };

      this.mailDeleted = function(ev, data) {
        if (_.contains(_.pluck(data.mails, 'ident'),  this.attr.mail.ident)) {
          this.openNoMessageSelectedPane();
        }
      };

      this.fetchMailToShow = function () {
        this.trigger(events.mail.want, {mail: this.attr.ident, caller: this});
      };

      this.after('initialize', function () {
        this.on(this, events.mail.here, this.displayMail);
        this.on(this, events.mail.notFound, this.openNoMessageSelectedPane);
        this.on(document, events.dispatchers.rightPane.clear, this.teardown);
        this.on(document, events.mail.tags.updated, this.tagsUpdated);
        this.on(document, events.mail.deleted, this.mailDeleted);
        this.fetchMailToShow();
      });
    }
  }
);
