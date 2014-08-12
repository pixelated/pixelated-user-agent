/*global Pixelated */
/*global _ */
/*global Bloodhound */

'use strict';

define(
  [
    'flight/lib/component',
    'views/templates',
    'mail_view/ui/mail_actions',
    'helpers/view_helper',
    'mixins/with_hide_and_show',
    'mixins/with_mail_tagging',
    'page/events',
    'views/i18n',
    'features'
  ],

  function (defineComponent, templates, mailActions, viewHelpers, withHideAndShow, withMailTagging, events, i18n, features) {

    return defineComponent(mailView, mailActions, withHideAndShow, withMailTagging);

    function mailView() {
      this.defaultAttrs({
        tags: '.tag',
        newTagInput: '#new-tag-input',
        newTagButton: '#new-tag-button',
        addNew: '.add-new',
        deleteModal: '#delete-modal',
        trashButton: '#trash-button',
        archiveButton: '#archive-button',
        closeModalButton: '.close-reveal-modal',
        closeMailButton: '.close-mail-button'
      });

      this.displayMail = function (event, data) {
        this.attr.mail = data.mail;

        var date = new Date(data.mail.header.date);
        data.mail.header.formattedDate = viewHelpers.getFormattedDate(date);

        data.mail.security_casing = data.mail.security_casing || {};
        if(features.isEnabled('signatureStatus')) {
          var signed = this.checkSigned(data.mail);
        }
        if(features.isEnabled('encryptionStatus')) {
          var encrypted = this.checkEncrypted(data.mail);
        }

        this.$node.html(templates.mails.fullView({
          header: data.mail.header,
          body: [],
          statuses: viewHelpers.formatStatusClasses(data.mail.status),
          ident: data.mail.ident,
          tags: data.mail.tags,
          encryptionStatus: encrypted,
          signatureStatus: signed,
          features: features
        }));

        this.$node.find('.bodyArea').html(viewHelpers.formatMailBody(data.mail));
        this.trigger(document, events.search.highlightResults, {where: '.bodyArea'});
        this.trigger(document, events.search.highlightResults, {where: '.subjectArea'});
        this.trigger(document, events.search.highlightResults, {where: '.msg-header .recipients'});

        this.attachTagCompletion();

        this.select('tags').on('click', function (event) {
          this.removeTag($(event.target).data('tag'));
        }.bind(this));

        this.addTagLoseFocus();
        this.on(this.select('newTagButton'), 'click', this.showNewTagInput);
        this.on(this.select('newTagInput'), 'keydown', this.handleKeyDown);
        this.on(this.select('newTagInput'), 'blur', this.addTagLoseFocus);
        this.on(this.select('trashButton'), 'click', this.moveToTrash);
        this.on(this.select('archiveButton'), 'click', this.archiveIt);
        this.on(this.select('closeModalButton'), 'click', this.closeModal);
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

        if(_.any(mail.security_casing.locks, function (lock) { return lock.state === 'valid'; })) { status.push('encryption-valid'); }
        else { status.push('encryption-failure'); }

        return status.join(' ');
      };

      this.checkSigned = function(mail) {
        if(_.isEmpty(mail.security_casing.imprints)) { return 'not-signed'; }

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
          this.createNewTag();
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
        var filteredTags = _.without(this.attr.mail.tags, tag);
        if (_.isEmpty(filteredTags)){
          this.displayMail({}, { mail: this.attr.mail });
          this.select('deleteModal').foundation('reveal', 'open');
        } else {
          this.updateTags(this.attr.mail, filteredTags);
        }
      };

      this.moveToTrash = function(){
        this.closeModal();
        this.trigger(document, events.ui.mail.delete, { mail: this.attr.mail });
      };

      this.archiveIt = function() {
        this.updateTags(this.attr.mail, []);
        this.closeModal();
        this.trigger(document, events.ui.userAlerts.displayMessage, { message: i18n.get('Your message was archive it!') });
        this.openNoMessageSelectedPane();
      };

      this.closeModal = function() {
        $('#delete-modal').foundation('reveal', 'close');
      };

      this.tagsUpdated = function(ev, data) {
        data = data || {};
        this.attr.mail.tags = data.tags;
        this.displayMail({}, { mail: this.attr.mail });
        this.trigger(document, events.ui.tagList.refresh);
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
