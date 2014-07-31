/*global Smail */
/*global jasmine */
/*global runs */
/*global waits */

describeMixin('mixins/with_mail_edit_base', function () {
  'use strict';

  beforeEach(function () {
    setupComponent();
    // Stubing mixing wrongly!!! 'deprecated' while waiting for draft component extraction
    this.component.buildMail = function (tag) {
      return { header: { to: ['a@smth.com'], from: 'b@smth.com', subject: 'Sbject' } };
    };
  });

  describe('initialization', function() {
    it('should enable send button when rendering with recipients', function() {
      var enableSendButtonEvent = spyOnEvent(document, Smail.events.ui.sendbutton.enable);

      this.component.render(function() {}, {
        recipients: { to: ['foobar@mail.com'], cc: [] }
      });

      expect(enableSendButtonEvent).toHaveBeenTriggeredOn(document);
    });

    it('should not enable send button when rendering without recipients', function() {
      var enableSendButtonEvent = spyOnEvent(document, Smail.events.ui.sendbutton.enable);

      this.component.render(function() {}, {
        recipients: { to: [], cc: [] }
      });

      expect(enableSendButtonEvent).not.toHaveBeenTriggeredOn(document);
    });
  });

  describe('when the user is typing in subject or body', function() {
    beforeEach(function () {
      this.component.attr.saveDraftInterval = 10;
    });

    it('saves the draft after the save draft interval number of seconds', function() {
      var saveDraftSpy = spyOnEvent(document, Smail.events.mail.saveDraft);
      runs(function () {
        this.component.monitorInput();
        expect(saveDraftSpy).not.toHaveBeenTriggeredOn(document);
      });
      waits(10);
      runs(function () {
        expect(saveDraftSpy).toHaveBeenTriggeredOn(document);
      });
    });

    it('does not save if mail is sent before the save draft interval number of seconds', function() {
      var saveDraftSpy = spyOnEvent(document, Smail.events.mail.saveDraft);
      runs(function () {
        this.component.monitorInput();
        this.component.sendMail();
      });
      waits(10);
      runs(function () {
        expect(saveDraftSpy).not.toHaveBeenTriggeredOn(document);
      });
    });
  });

  describe('when a mail is sent', function () {
    it('displays a message of mail sent', function () {
      var spy = spyOnEvent(document, Smail.events.ui.userAlerts.displayMessage);
      this.component.trigger(document, Smail.events.mail.sent);
      expect(spy).toHaveBeenTriggeredOn(document);
    });
  });

  describe('when user asks to trash the mail', function() {
    it('triggers mail delete for this mail', function() {
      var spy = spyOnEvent(document, Smail.events.mail.save);
      this.component.trashMail();
      expect(spy).toHaveBeenTriggeredOn(document);
    });
  });

  describe('when recipients are updated', function () {
    it('triggers an event to let the send button know that the recipients in the mail are updated', function () {
      var uiMailRecipientsUpdated = spyOnEvent(document, Smail.events.ui.mail.recipientsUpdated);

      $(document).trigger(Smail.events.ui.recipients.updated, {recipientsName: 'to', newRecipients: ['fox@somewhere.com']});

      expect(uiMailRecipientsUpdated).toHaveBeenTriggeredOn(document);
    });
  });
});
