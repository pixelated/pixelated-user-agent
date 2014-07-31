/*global Smail */

describeComponent('mail_view/data/mail_sender', function () {
  'use strict';

  var mailBuilder;
  var mail;

  beforeEach(function () {
    mailBuilder =  require('mail_view/data/mail_builder');
    mail = Smail.testData().parsedMail.simpleTextPlain;
    setupComponent();
  });

  it('sends mail data with a POST to the server when asked to send email', function() {
    var mailSentEventSpy = spyOnEvent(document, Smail.events.mail.sent);
    var g;

    spyOn($, 'ajax').andReturn({done: function(f) { g = f; return {fail: function(){}};}});

    this.component.trigger(Smail.events.mail.send, mail);

    g();

    expect(mailSentEventSpy).toHaveBeenTriggeredOn(document);

    expect($.ajax.mostRecentCall.args[0]).toEqual('/mails');
    expect($.ajax.mostRecentCall.args[1].type).toEqual('POST');
    expect(JSON.parse($.ajax.mostRecentCall.args[1].data).header).toEqual(mail.header);
    expect(JSON.parse($.ajax.mostRecentCall.args[1].data).body).toEqual(mail.body);
  });

  it('save draft data with a POST to the server when asked to save draft for the first time', function() {
    var draftSavedEventSpy = spyOnEvent(document, Smail.events.mail.draftSaved);
    var g;

    spyOn($, 'ajax').andReturn({done: function(f) { g = f; return {fail: function(){}};}});

    mail.ident = '';
    this.component.trigger(Smail.events.mail.saveDraft, mail);

    g();

    expect(draftSavedEventSpy).toHaveBeenTriggeredOn(document);

    expect($.ajax.mostRecentCall.args[0]).toEqual('/mails');
    expect($.ajax.mostRecentCall.args[1].type).toEqual('POST');
    expect(JSON.parse($.ajax.mostRecentCall.args[1].data).header).toEqual(mail.header);
    expect(JSON.parse($.ajax.mostRecentCall.args[1].data).body).toEqual(mail.body);
  });

  it('save draft data with a PUT to the server when asked to save draft for the second time', function() {
    var draftSavedEventSpy = spyOnEvent(document, Smail.events.mail.draftSaved);
    var g;

    spyOn($, 'ajax').andReturn({done: function(f) { g = f; return {fail: function(){}};}});

    mail.ident = 0;
    this.component.trigger(Smail.events.mail.saveDraft, mail);

    g();

    expect(draftSavedEventSpy).toHaveBeenTriggeredOn(document);

    expect($.ajax.mostRecentCall.args[0]).toEqual('/mails');
    expect($.ajax.mostRecentCall.args[1].type).toEqual('PUT');
    expect(JSON.parse($.ajax.mostRecentCall.args[1].data).header).toEqual(mail.header);
    expect(JSON.parse($.ajax.mostRecentCall.args[1].data).body).toEqual(mail.body);
  });
});
