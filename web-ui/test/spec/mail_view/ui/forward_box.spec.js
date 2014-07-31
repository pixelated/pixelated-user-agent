/*global jasmine */
/*global Smail */

describeComponent('mail_view/ui/forward_box', function () {
  'use strict';

  var attrs;
  var testMail;
  beforeEach(function () {
    testMail = Smail.testData().parsedMail.simpleTextPlain;

    Smail.mockBloodhound();
  });

  it('should have a subject of Fwd: <original_message>', function() {
    testMail.header.subject = 'Very interesting';
    setupComponent({ mail: testMail });

    expect(this.component.select('subjectDisplay').text()).toEqual('Fwd: '+ testMail.header.subject);
  });

  it('should have no recipients', function () {
    var Recipients = require('mail_view/ui/recipients/recipients');
    spyOn(Recipients, 'attachTo');

    setupComponent({ mail: testMail });

    expect(Recipients.attachTo.calls[0].args[1]).toEqual({name: 'to', addresses: []});
    expect(Recipients.attachTo.calls[1].args[1]).toEqual({name: 'cc', addresses: []});
    expect(Recipients.attachTo.calls[2].args[1]).toEqual({name: 'bcc', addresses: []});
  });

  it('should populate body text area with quote of email being forwarded', function() {
    var viewHelper = require('helpers/view_helper');
    spyOn(viewHelper, 'quoteMail').andReturn('quoted email');

    setupComponent({ mail: testMail });

    expect(viewHelper.quoteMail).toHaveBeenCalledWith(testMail);
    expect(this.component.select('bodyBox').val()).toBe('quoted email');
  });

  it('should show subject field when clicking on subject display', function() {
    setupComponent({ mail: testMail });

    this.component.select('subjectDisplay').click();

    expect(this.component.select('subjectInput')).not.toBeHidden();
    expect(this.component.select('subjectDisplay')).toBeHidden();
  });

  it('should copy original message headers', function() {
    var mailSendEvent = spyOnEvent(document, Smail.events.mail.send);

    testMail.header.bcc = 'original_bcc@email.com';
    testMail.header.cc = 'original_cc@email.com';
    testMail.header.date = 'original_date';
    testMail.header.from = 'original_from';
    testMail.header.message_id = 'original_message_id';
    testMail.header.reply_to = 'original_reply_to@email.com';
    testMail.header.sender = 'original_sender';
    testMail.header.to = 'original_to@email.com';

    setupComponent({ mail: testMail });

    this.component.attr.recipientValues.to.push('forward_to@email.com');
    $(document).trigger(Smail.events.ui.mail.send);

    expect(mailSendEvent).toHaveBeenTriggeredOn(document);
    var sentMail = mailSendEvent.mostRecentCall.data;

    expect(sentMail.header).toEqual(jasmine.objectContaining({
      resent_bcc: 'original_bcc@email.com',
      resent_cc: 'original_cc@email.com',
      resent_date: 'original_date',
      resent_from: 'original_from',
      resent_message_id: 'original_message_id',
      resent_reply_to: 'original_reply_to@email.com',
      resent_sender: 'original_sender',
      resent_to: 'original_to@email.com'
    }));
  });

  it('triggers openMail when email is sent', function() {
    var eventSpy = spyOnEvent(document, Smail.events.ui.mail.open);
    setupComponent({ mail: testMail });
    $(document).trigger(Smail.events.mail.sent, {ident: testMail.ident});
    expect(eventSpy).toHaveBeenTriggeredOnAndWith(document, {ident: testMail.ident});
  });
});
