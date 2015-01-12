describeMixin('mixins/with_mail_edit_base', function () {
  'use strict';

  beforeEach(function () {
    this.setupComponent();
    // Stubing mixing wrongly!!! 'deprecated' while waiting for draft component extraction
    this.component.buildMail = function (tag) {
      return { header: { to: ['a@smth.com'], from: 'b@smth.com', subject: 'Sbject' } };
    };
  });

  describe('initialization', function() {

    it('should warn send button of existing recipients', function () {
      var recipientsUpdatedEvent = spyOnEvent(document, Pixelated.events.ui.recipients.updated);

      this.component.render(function() {}, {
        recipients: { to: ['foobar@mail.com'], cc: [] }
      });

      expect(recipientsUpdatedEvent).toHaveBeenTriggeredOnAndWith(document, { newRecipients: ['foobar@mail.com'], name: 'to'});
      expect(recipientsUpdatedEvent).not.toHaveBeenTriggeredOnAndWith(document, { newRecipients: [], name: 'cc'});
    });

  });

  describe('when the user is typing in subject or body', function() {
    beforeEach(function () {
      this.component.attr.saveDraftInterval = 10;
    });

    it('saves the draft after the save draft interval number of seconds', function(done) {
      var saveDraftSpy = spyOnEvent(document, Pixelated.events.mail.saveDraft);
      this.component.monitorInput();
      expect(saveDraftSpy).not.toHaveBeenTriggeredOn(document);

      setTimeout(function () {
        expect(saveDraftSpy).toHaveBeenTriggeredOn(document);
        done();
      }, 10);
    });

    it('does not save if mail is sent before the save draft interval number of seconds', function(done) {
      var saveDraftSpy = spyOnEvent(document, Pixelated.events.mail.saveDraft);
      this.component.monitorInput();
      this.component.sendMail();

      setTimeout(function () {
        expect(saveDraftSpy).not.toHaveBeenTriggeredOn(document);
        done();
      }, 10);
    });
  });

  describe('when a mail is sent', function () {
    it('displays a message of mail sent', function () {
      var spy = spyOnEvent(document, Pixelated.events.ui.userAlerts.displayMessage);
      this.component.trigger(document, Pixelated.events.mail.sent);
      expect(spy).toHaveBeenTriggeredOn(document);
    });
  });

  describe('when user asks to trash the mail', function() {
    it('triggers mail delete for this mail', function() {
      var spy = spyOnEvent(document, Pixelated.events.mail.save);
      this.component.trashMail();
      expect(spy).toHaveBeenTriggeredOn(document);
    });
  });

  describe('when recipients are updated', function () {
    it('triggers an event to let the send button know that the recipients in the mail are updated', function () {
      var uiMailRecipientsUpdated = spyOnEvent(document, Pixelated.events.ui.mail.recipientsUpdated);

      $(document).trigger(Pixelated.events.ui.recipients.updated, {recipientsName: 'to', newRecipients: ['fox@somewhere.com']});

      expect(uiMailRecipientsUpdated).toHaveBeenTriggeredOn(document);
    });
  });
});
