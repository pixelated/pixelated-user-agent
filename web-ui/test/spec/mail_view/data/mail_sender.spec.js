describeComponent('mail_view/data/mail_sender', function () {
  'use strict';

  var mailBuilder;
  var mail;

  beforeEach(function () {
    mailBuilder =  require('mail_view/data/mail_builder');
    mail = Pixelated.testData().parsedMail.simpleTextPlain;
    this.setupComponent();
  });

  it('sends mail data with a POST to the server when asked to send email', function() {
    var mailSentEventSpy = spyOnEvent(document, Pixelated.events.mail.sent);
    var deferred = $.Deferred();

    spyOn($, 'ajax').and.returnValue(deferred);

    this.component.trigger(Pixelated.events.mail.send, mail);

    deferred.resolve();

    expect(mailSentEventSpy).toHaveBeenTriggeredOn(document);

    expect($.ajax.calls.mostRecent().args[0]).toEqual('/mails');
    expect($.ajax.calls.mostRecent().args[1].type).toEqual('POST');
    expect(JSON.parse($.ajax.calls.mostRecent().args[1].data).header).toEqual(mail.header);
    expect(JSON.parse($.ajax.calls.mostRecent().args[1].data).body).toEqual(mail.body);
  });

  it('save draft data with a PUT to the server', function() {
    var draftSavedEventSpy = spyOnEvent(document, Pixelated.events.mail.draftSaved);
    var deferred = $.Deferred();

    spyOn($, 'ajax').and.returnValue(deferred);

    mail.ident = 0;
    this.component.trigger(Pixelated.events.mail.saveDraft, mail);

    deferred.resolve();

    expect(draftSavedEventSpy).toHaveBeenTriggeredOn(document);

    expect($.ajax.calls.mostRecent().args[0]).toEqual('/mails');
    expect($.ajax.calls.mostRecent().args[1].type).toEqual('PUT');
    expect(JSON.parse($.ajax.calls.mostRecent().args[1].data).header).toEqual(mail.header);
    expect(JSON.parse($.ajax.calls.mostRecent().args[1].data).body).toEqual(mail.body);
  });

  it('uses the monitored ajax call to delegate for errors', function () {
    var monitoredAjaxCall = require('helpers/monitored_ajax');
    spyOn(monitoredAjaxCall, 'call').and.returnValue($.Deferred());

    this.component.trigger(Pixelated.events.mail.send, mail);
    this.component.trigger(Pixelated.events.mail.saveDraft, mail);

    expect(monitoredAjaxCall.call.calls.count()).toEqual(2);
  });

});
