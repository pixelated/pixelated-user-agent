describeComponent('mail_view/ui/compose_box', function () {
  'use strict';
  beforeEach(function () {
    Pixelated.mockBloodhound();
    this.setupComponent('<div style="display:none"></div>');
  });


  describe('compose new mail', function() {

    it('only sends if all the recipients are valid emails', function() {
      $(document).trigger(Pixelated.events.ui.recipients.updated, {recipientsName: 'to', newRecipients: ['valid@email.example']});

      var eventSpy = spyOnEvent(document, Pixelated.events.mail.send);

      $(document).trigger(Pixelated.events.ui.mail.send);

      expect(eventSpy).toHaveBeenTriggeredOn(document);
    });

    it('sends the recipient entered', function () {
      $(document).trigger(Pixelated.events.ui.recipients.updated, {recipientsName: 'to', newRecipients: ['fox@somewhere.com']});

      var eventSpy = spyOnEvent(document, Pixelated.events.mail.send);

      $(document).trigger(Pixelated.events.ui.mail.send);

      expect(eventSpy).toHaveBeenTriggeredOn(document);
      expect(eventSpy.mostRecentCall.data.header).toEqual(jasmine.objectContaining({
        to: ['fox@somewhere.com']
      }));
    });

    it('sends the multiple recipients entered', function () {
      $(document).trigger(Pixelated.events.ui.recipients.updated, {recipientsName: 'to', newRecipients: ['fox@somewhere.com', 'blarg@someone.com', 'fox2@google.se']});
      var eventSpy = spyOnEvent(document, Pixelated.events.mail.send);

      $(document).trigger(Pixelated.events.ui.mail.send);

      expect(eventSpy).toHaveBeenTriggeredOn(document);
      expect(eventSpy.mostRecentCall.data.header).toEqual(jasmine.objectContaining({
        to: ['fox@somewhere.com', 'blarg@someone.com', 'fox2@google.se']
      }));
    });

    it('sends the subject line entered', function () {
      $(document).trigger(Pixelated.events.ui.recipients.updated, {recipientsName: 'to', newRecipients: ['aa@aa.com']});
      this.component.select('subjectBox').val('A new fancy subject!');
      var eventSpy = spyOnEvent(document, Pixelated.events.mail.send);

      $(document).trigger(Pixelated.events.ui.mail.send);

      expect(eventSpy).toHaveBeenTriggeredOn(document);
      expect(eventSpy.mostRecentCall.data.header).toEqual(jasmine.objectContaining({
        subject: 'A new fancy subject!'
      }));
    });

    it('sends the multiple CCs entered', function () {
      $(document).trigger(Pixelated.events.ui.recipients.updated, {recipientsName: 'cc', newRecipients: ['cc1@foo.bar', 'cc2@bar.foo', 'cc3@zz.top']});
      var eventSpy = spyOnEvent(document, Pixelated.events.mail.send);

      $(document).trigger(Pixelated.events.ui.mail.send);

      expect(eventSpy).toHaveBeenTriggeredOn(document);
      expect(eventSpy.mostRecentCall.data.header).toEqual(jasmine.objectContaining({
        cc: ['cc1@foo.bar', 'cc2@bar.foo', 'cc3@zz.top']
      }));
    });

    it('sends the multiple BCCs entered', function () {
      $(document).trigger(Pixelated.events.ui.recipients.updated, {recipientsName: 'bcc', newRecipients: ['bcc1@foo.bar', 'bcc2@bar.foo', 'bcc3@zz.top']});
      var eventSpy = spyOnEvent(document, Pixelated.events.mail.send);

      $(document).trigger(Pixelated.events.ui.mail.send);

      expect(eventSpy).toHaveBeenTriggeredOn(document);
      expect(eventSpy.mostRecentCall.data.header).toEqual(jasmine.objectContaining({
        bcc: ['bcc1@foo.bar', 'bcc2@bar.foo', 'bcc3@zz.top']
      }));
    });

    it('shows no message selected pane when deleting the email being composed', function() {
      var openNoMessageSelectedPaneEvent = spyOnEvent(document, Pixelated.events.dispatchers.rightPane.openNoMessageSelected);
      var mails = [{ident: 123}];
      this.component.attr.ident = 123;

      this.component.trigger(document, Pixelated.events.mail.deleted, {mails: mails});

      expect(openNoMessageSelectedPaneEvent).toHaveBeenTriggeredOn(document);
    });

    it('does not show no message selected pane when deleting a different set of emails', function() {
      var openNoMessageSelectedPaneEvent = spyOnEvent(document, Pixelated.events.dispatchers.rightPane.openNoMessageSelected);
      var mails = [{ident: 321}];
      this.component.attr.ident = 123;

      this.component.trigger(document, Pixelated.events.mail.deleted, {mails: mails});

      expect(openNoMessageSelectedPaneEvent).not.toHaveBeenTriggeredOn(document);
    });

    it('should call the enableFloatlabel method when events.mail.here is trigged', function() {
      spyOn(this.component, 'enableFloatlabel');

      this.component.renderComposeBox();

      expect(this.component.enableFloatlabel).toHaveBeenCalledWith('input.floatlabel');
      expect(this.component.enableFloatlabel).toHaveBeenCalledWith('textarea.floatlabel');
    });
  });

  describe('close button behavior', function() {

    it('should fire Show no message selected if the close button is clicked', function() {
      var spy = spyOnEvent(document, Pixelated.events.dispatchers.rightPane.openNoMessageSelected);
      this.component.select('closeButton').click();
      expect(spy).toHaveBeenTriggeredOn(document);
    });

  });

  describe('draft compose box', function() {
    it('should save a draft when click on draft button', function () {
      $(document).trigger(Pixelated.events.ui.recipients.updated, {recipientsName: 'to', newRecipients: ['fox@somewhere.com']});

      this.component.select('subjectBox').val('A new fancy subject!');
      var eventSpy = spyOnEvent(document, Pixelated.events.mail.saveDraft);

      this.component.select('draftButton').click();

      expect(eventSpy).toHaveBeenTriggeredOn(document);
      expect(eventSpy.mostRecentCall.data.header).toEqual(jasmine.objectContaining({
        to: ['fox@somewhere.com']
      }));
    });
  });

  describe('subject label', function() {
    var input;
    var label;

    beforeEach(function() {
      input = $(this.component.$node).find('input');
      label = input.prev('label');

      this.component.enableFloatlabel(input);
    });

    it('should show the subject label after the user starts typing', function() {
      input.val('test');
      input.trigger('keyup');

      expect(input.hasClass('showfloatlabel')).toEqual(true);
      expect(label.hasClass('showfloatlabel')).toEqual(true);
    });

    it('should not show the subject label if the field is empty', function() {
      input.val('');
      input.trigger('keyup');

      expect(input.hasClass('showfloatlabel')).toEqual(false);
      expect(label.hasClass('showfloatlabel')).toEqual(false);
    });
  });

  describe('body label', function() {
    var textarea;
    var label;

    beforeEach(function() {
      textarea = $(this.component.$node).find('textarea');
      label = textarea.prev('label');

      this.component.enableFloatlabel(textarea);
    });

    it('should show the subject label after the user starts typing', function() {
      textarea.text('test');
      textarea.trigger('keyup');

      expect(textarea.hasClass('showfloatlabel')).toEqual(true);
      expect(label.hasClass('showfloatlabel')).toEqual(true);
    });

    it('should not show the subject label if the field is empty', function() {
      textarea.text('');
      textarea.trigger('keyup');

      expect(textarea.hasClass('showfloatlabel')).toEqual(false);
      expect(label.hasClass('showfloatlabel')).toEqual(false);
    });
  });
});
