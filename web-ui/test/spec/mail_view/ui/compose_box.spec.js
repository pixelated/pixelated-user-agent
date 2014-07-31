/*global jasmine */
/*global Smail */

describeComponent('mail_view/ui/compose_box', function () {
  'use strict';
  beforeEach(function () {
    Smail.mockBloodhound();
    setupComponent('<div style="display:none"></div>');
  });


  describe('compose new mail', function() {

    it('only sends if all the recipients are valid emails', function() {
      $(document).trigger(Smail.events.ui.recipients.updated, {recipientsName: 'to', newRecipients: ['valid@email.example']});

      var eventSpy = spyOnEvent(document, Smail.events.mail.send);

      $(document).trigger(Smail.events.ui.mail.send);

      expect(eventSpy).toHaveBeenTriggeredOn(document);
    });

    it('sends the recipient entered', function () {
      $(document).trigger(Smail.events.ui.recipients.updated, {recipientsName: 'to', newRecipients: ['fox@somewhere.com']});

      var eventSpy = spyOnEvent(document, Smail.events.mail.send);

      $(document).trigger(Smail.events.ui.mail.send);

      expect(eventSpy).toHaveBeenTriggeredOn(document);
      expect(eventSpy.mostRecentCall.data.header).toEqual(jasmine.objectContaining({
        to: ['fox@somewhere.com']
      }));
    });

    it('sends the multiple recipients entered', function () {
      $(document).trigger(Smail.events.ui.recipients.updated, {recipientsName: 'to', newRecipients: ['fox@somewhere.com', 'blarg@someone.com', 'fox2@google.se']});
      var eventSpy = spyOnEvent(document, Smail.events.mail.send);

      $(document).trigger(Smail.events.ui.mail.send);

      expect(eventSpy).toHaveBeenTriggeredOn(document);
      expect(eventSpy.mostRecentCall.data.header).toEqual(jasmine.objectContaining({
        to: ['fox@somewhere.com', 'blarg@someone.com', 'fox2@google.se']
      }));
    });

    it('sends the subject line entered', function () {
      $(document).trigger(Smail.events.ui.recipients.updated, {recipientsName: 'to', newRecipients: ['aa@aa.com']});
      this.component.select('subjectBox').val('A new fancy subject!');
      var eventSpy = spyOnEvent(document, Smail.events.mail.send);

      $(document).trigger(Smail.events.ui.mail.send);

      expect(eventSpy).toHaveBeenTriggeredOn(document);
      expect(eventSpy.mostRecentCall.data.header).toEqual(jasmine.objectContaining({
        subject: 'A new fancy subject!'
      }));
    });

    it('sends the multiple CCs entered', function () {
      $(document).trigger(Smail.events.ui.recipients.updated, {recipientsName: 'cc', newRecipients: ['cc1@foo.bar', 'cc2@bar.foo', 'cc3@zz.top']});
      var eventSpy = spyOnEvent(document, Smail.events.mail.send);

      $(document).trigger(Smail.events.ui.mail.send);

      expect(eventSpy).toHaveBeenTriggeredOn(document);
      expect(eventSpy.mostRecentCall.data.header).toEqual(jasmine.objectContaining({
        cc: ['cc1@foo.bar', 'cc2@bar.foo', 'cc3@zz.top']
      }));
    });

    it('sends the multiple BCCs entered', function () {
      $(document).trigger(Smail.events.ui.recipients.updated, {recipientsName: 'bcc', newRecipients: ['bcc1@foo.bar', 'bcc2@bar.foo', 'bcc3@zz.top']});
      var eventSpy = spyOnEvent(document, Smail.events.mail.send);

      $(document).trigger(Smail.events.ui.mail.send);

      expect(eventSpy).toHaveBeenTriggeredOn(document);
      expect(eventSpy.mostRecentCall.data.header).toEqual(jasmine.objectContaining({
        bcc: ['bcc1@foo.bar', 'bcc2@bar.foo', 'bcc3@zz.top']
      }));
    });

    it('shows no message selected pane when deleting the email being composed', function() {
      var openNoMessageSelectedPaneEvent = spyOnEvent(document, Smail.events.dispatchers.rightPane.openNoMessageSelected);
      var mails = [{ident: 123}];
      this.component.attr.ident = 123;

      this.component.trigger(document, Smail.events.mail.deleted, {mails: mails});

      expect(openNoMessageSelectedPaneEvent).toHaveBeenTriggeredOn(document);
    });

    it('does not show no message selected pane when deleting a different set of emails', function() {
      var openNoMessageSelectedPaneEvent = spyOnEvent(document, Smail.events.dispatchers.rightPane.openNoMessageSelected);
      var mails = [{ident: 321}];
      this.component.attr.ident = 123;

      this.component.trigger(document, Smail.events.mail.deleted, {mails: mails});

      expect(openNoMessageSelectedPaneEvent).not.toHaveBeenTriggeredOn(document);
    });
  });

  describe('close button behavior', function() {

    it('should fire Show no message selected if the close button is clicked', function() {
      var spy = spyOnEvent(document, Smail.events.dispatchers.rightPane.openNoMessageSelected);
      this.component.select('closeButton').click();
      expect(spy).toHaveBeenTriggeredOn(document);
    });

  });

  describe('draft compose box', function() {
    it('should save a draft when click on draft button', function () {
      $(document).trigger(Smail.events.ui.recipients.updated, {recipientsName: 'to', newRecipients: ['fox@somewhere.com']});

      this.component.select('subjectBox').val('A new fancy subject!');
      var eventSpy = spyOnEvent(document, Smail.events.mail.saveDraft);

      this.component.select('draftButton').click();

      expect(eventSpy).toHaveBeenTriggeredOn(document);
      expect(eventSpy.mostRecentCall.data.header).toEqual(jasmine.objectContaining({
        to: ['fox@somewhere.com']
      }));
    });
  });
});
