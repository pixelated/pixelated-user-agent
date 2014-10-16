/*global jasmine */
/*global Pixelated */
'use strict';

describeComponent('services/mail_service', function () {

  var email1, i18n;

  beforeEach( function () {
    setupComponent();
    email1 = Pixelated.testData().parsedMail.simpleTextPlain;
    i18n = require('views/i18n');
  } );

  it('marks the desired message as read', function () {
    var readRequest = spyOn($, 'ajax').andReturn({});

    this.component.trigger(Pixelated.events.mail.read, {ident: 1});

    expect(readRequest.mostRecentCall.args[0]).toEqual('/mail/1/read');
  });

  describe('when marks many emails as read', function () {
    var readRequest, checkedMails, uncheckedEmailsEvent, setCheckAllEvent, doneMarkAsRead;

    beforeEach(function () {
      readRequest = spyOn($, 'ajax').andReturn({done: function(f) { doneMarkAsRead = f; return {fail: function() {}};}});
      uncheckedEmailsEvent = spyOnEvent(document, Pixelated.events.ui.mail.unchecked);
      setCheckAllEvent = spyOnEvent(document, Pixelated.events.ui.mails.hasMailsChecked);
      spyOn(this.component, 'refreshResults');

      checkedMails = {
        1: {ident: 1},
        2: {ident: 2}
      };

      this.component.trigger(Pixelated.events.mail.read, {checkedMails: checkedMails});
    });

    it('makes the correct request to the backend', function () {
      expect(readRequest.mostRecentCall.args[0]).toEqual('/mails/read');
      expect(readRequest.mostRecentCall.args[1].data).toEqual({idents: '[1,2]'});
    });

    it('will trigger that a message has been deleted when it is done deleting', function() {
      doneMarkAsRead({mails: checkedMails});
      expect(this.component.refreshResults).toHaveBeenCalled();
    });

    it('unchecks read emails', function () {
      doneMarkAsRead({mails: checkedMails});
      expect(uncheckedEmailsEvent).toHaveBeenTriggeredOnAndWith(document, {mails: checkedMails});
    });

    it('clears the check all checkbox', function () {
      doneMarkAsRead({mails: checkedMails});
      expect(setCheckAllEvent).toHaveBeenTriggeredOnAndWith(document, false);
    });
  });

  it('fetches a single email', function () {
    var me = {};
    var spyAjax = spyOn($, 'ajax').andReturn({done: function(f) { f(email1); return {fail: function() {}};}});
    var mailHereEvent = spyOnEvent(me, Pixelated.events.mail.here);

    this.component.trigger(Pixelated.events.mail.want, { caller: me, mail: email1.ident });

    expect(mailHereEvent).toHaveBeenTriggeredOn(me);
    expect(spyAjax.mostRecentCall.args[0]).toEqual('/mail/' + email1.ident);
  });

  it('answers mail:notFound if mail returned from server is null', function () {
    var me = {};
    var spyAjax = spyOn($, 'ajax').andReturn({done: function(f) { f(null); return {fail: function() {}};}});
    var mailNotFound = spyOnEvent(me, Pixelated.events.mail.notFound);

    this.component.trigger(Pixelated.events.mail.want, { caller: me, mail: email1.ident });

    expect(mailNotFound).toHaveBeenTriggeredOn(me);
  });

  it('updates the tags of the desired message', function () {
    spyOn(this.component, 'refreshResults');
    var updateTagsReturnValue = { tags: ['website'], mailbox: 'inbox'}
    var spyAjax = spyOn($, 'ajax').andReturn({done: function(f) { f(updateTagsReturnValue); return {fail: function() {}};}});

    var spyEvent = spyOnEvent(document, Pixelated.events.mail.tags.updated);
    var component = jasmine.createSpyObj('component',['successUpdateTags']);
    spyOn(this.component, 'fetchMail');

    this.component.trigger(Pixelated.events.mail.tags.update, { ident: email1.ident, tags: email1.tags });

    expect(spyEvent).toHaveBeenTriggeredOn(document);
    expect(spyAjax.calls[0].args[0]).toEqual('/mail/1/tags');
    expect(spyAjax.calls[0].args[1].data).toEqual(JSON.stringify({ newtags: email1.tags } ));
    expect(this.component.refreshResults).toHaveBeenCalled();
  });

  it('triggers an error message when it can\'t update the tags', function () {
    var spyAjax = spyOn($, 'ajax').andReturn({done: function() { return {fail: function(f) {f({status:500});}};}});

    var spyEvent = spyOnEvent(document, Pixelated.events.ui.userAlerts.displayMessage);
    var component = jasmine.createSpyObj('component',['failureUpdateTags']);

    this.component.trigger(Pixelated.events.mail.tags.update, { ident: email1.ident, tags: email1.tags });

    expect(spyEvent).toHaveBeenTriggeredOn(document);
    expect(spyAjax.mostRecentCall.args[0]).toEqual('/mail/1/tags');
    expect(spyAjax.mostRecentCall.args[1].data).toEqual(JSON.stringify({ newtags: email1.tags } ));
  });

  it('will try to delete a message when requested to', function() {
    var spyAjax = spyOn($, 'ajax').andReturn({done: function() { return {fail: function(f) {}};}});
    this.component.trigger(Pixelated.events.mail.delete, {mail: {ident: '43'}});
    expect(spyAjax).toHaveBeenCalled();
    expect(spyAjax.mostRecentCall.args[0]).toEqual('/mail/43');
    expect(spyAjax.mostRecentCall.args[1].type).toEqual('DELETE');
  });

  describe('when successfuly deletes an email', function () {
    var displayMessageEvent, uncheckedEmailsEvent, setCheckAllEvent, mailsDeletedEvent;

    beforeEach(function () {
      displayMessageEvent = spyOnEvent(document, Pixelated.events.ui.userAlerts.displayMessage);
      uncheckedEmailsEvent = spyOnEvent(document, Pixelated.events.ui.mail.unchecked);
      setCheckAllEvent = spyOnEvent(document, Pixelated.events.ui.mails.hasMailsChecked);
      mailsDeletedEvent = spyOnEvent(document, Pixelated.events.mail.deleted);
      spyOn(this.component, 'refreshResults');

      this.component.triggerDeleted({
        successMessage: 'A success message',
        mails: {1: 'email 1', 2: 'email 2'}
      })();
    });

    it('will trigger that a message has been deleted when it is done deleting', function() {
      expect(this.component.refreshResults).toHaveBeenCalled();
    });

    it('displays a success message', function () {
      expect(displayMessageEvent).toHaveBeenTriggeredOnAndWith(document, {message: 'A success message'});
    });

    it('unchecks deleted emails', function () {
      expect(uncheckedEmailsEvent).toHaveBeenTriggeredOnAndWith(document, { mails: {1: 'email 1', 2: 'email 2'} });
    });

    it('tells about deleted emails', function () {
      expect(mailsDeletedEvent).toHaveBeenTriggeredOnAndWith(document, { mails: {1: 'email 1', 2: 'email 2'} });
    });

    it('clears the check all checkbox', function () {
      expect(setCheckAllEvent).toHaveBeenTriggeredOnAndWith(document, false);
    });
  });

  it('will trigger an error message when a message cannot be deleted', function() {
    spyOn($, 'ajax').andReturn({done: function() { return {fail: function(f) { f(); }};}});
    var spyEvent = spyOnEvent(document, Pixelated.events.ui.userAlerts.displayMessage);

    this.component.trigger(Pixelated.events.mail.delete, {mail: {ident: '43'}});

    expect(spyEvent).toHaveBeenTriggeredOnAndWith(document, {message: i18n('Could not delete email')} );
  });

  it('triggers mails:available with received mails and keeps that tag as the current tag', function() {
    var g;
    var eventSpy = spyOnEvent(document, Pixelated.events.mails.available);

    spyOn($, 'ajax').andReturn({done: function(f) { g = f; return {fail: function(){}};}});
    this.component.trigger(Pixelated.events.ui.mails.fetchByTag, {tag: 'inbox'});

    g({stats: {}, mails: [email1]});
    expect(eventSpy.mostRecentCall.data.stats).toEqual({});
    expect(eventSpy.mostRecentCall.data.tag).toEqual('inbox');
    expect(this.component.attr.currentTag).toEqual('inbox');
  });

  it('wraps the tag in quotes before fetching by tag (to support tags with spaces)', function () {
    spyOn($, 'ajax').andReturn({done: function(f) { return {fail: function(){}};}});

    this.component.trigger(Pixelated.events.ui.mails.fetchByTag, {tag: 'new tag'});

    expect($.ajax.mostRecentCall.args[0]).toContain(encodeURI('tag:"new tag"'));
  });

  it('sends the previous tag when mails:refresh is called without a tag (this happens when the refresher calls it)', function () {
    var g;
    var eventSpy = spyOnEvent(document, Pixelated.events.mails.availableForRefresh);
    this.component.attr.currentTag = 'sent';

    spyOn($, 'ajax').andReturn({done: function(f) { g = f; return {fail: function(){}};}});
    this.component.trigger(Pixelated.events.ui.mails.refresh);

    g({stats: {}, mails: [email1]});
    expect(eventSpy.mostRecentCall.data.tag).toEqual('sent');
    expect(eventSpy.mostRecentCall.data.stats).toEqual({});
  });

  describe('pagination', function() {
    var pageChangedEvent;
    var g;

    beforeEach(function () {
      pageChangedEvent = spyOnEvent(document, Pixelated.events.ui.page.changed);
      spyOn($, 'ajax').andReturn({done: function(f) {
        g = f;
        return {fail: function(){}};
      }});
      spyOn(this.component, 'fetchMail').andCallThrough();
    });

    it('changes to the previous page and refetch email when ui:page:previous is fired', function() {
      this.component.attr.currentPage = 2;

      this.component.trigger(Pixelated.events.ui.page.previous);

      expect(this.component.fetchMail).toHaveBeenCalled();
      expect(this.component.attr.currentPage).toEqual(1);
    });

    it('won\'t change the page if it was already at the first page and trying to go to previous', function() {
      this.component.attr.currentPage = 1;

      this.component.trigger(Pixelated.events.ui.page.previous);

      expect(this.component.fetchMail).not.toHaveBeenCalled();
      expect(this.component.attr.currentPage).toEqual(1);
    });

    it('changes to the next page and refetch email when ui:page:next is fired', function() {
      this.component.attr.numPages = 10;
      this.component.attr.currentPage = 1;

      this.component.trigger(Pixelated.events.ui.page.next);

      expect(this.component.fetchMail).toHaveBeenCalled();
      expect(this.component.attr.currentPage).toEqual(2);
    });

    it('won\'t change the page if it is at the last mail when ui:page:next is fired', function() {
      this.component.attr.numPages = 9;
      this.component.attr.currentPage = 9;

      this.component.trigger(Pixelated.events.ui.page.next);

      expect(this.component.fetchMail).not.toHaveBeenCalled();
      expect(this.component.attr.currentPage).toEqual(9);
    });


    it('triggers pageChanged event when going to next page', function() {
      this.component.attr.numPages = 10;
      this.component.trigger(Pixelated.events.ui.page.next);

      expect(pageChangedEvent).toHaveBeenTriggeredOnAndWith(document, {currentPage: 2, numPages: 10});
    });

    it('triggers pageChanged event when going to previous page', function() {
      this.component.attr.numPages = 10;
      this.component.attr.currentPage = 2;
      this.component.trigger(Pixelated.events.ui.page.previous);

      expect(pageChangedEvent).toHaveBeenTriggeredOnAndWith(document, {currentPage: 1, numPages: 10});
    });

    it('resets currentPage when fetching mails by tag', function() {
      this.component.attr.numPages = 10;
      this.component.attr.currentPage = 999;
      this.component.trigger(Pixelated.events.ui.mails.fetchByTag, {tag: 'inbox'});

      expect(this.component.attr.currentPage).toEqual(1);
      expect(pageChangedEvent).toHaveBeenTriggeredOnAndWith(document, {currentPage: 1, numPages: 10});
    });

    describe('total page numbers', function() {
      var mailSetData = {
        tag: 'inbox',
        stats: { },
        mails: [],
        timing: {}
      };

      it('should have 5 pages with a 100 results and w 20', function() {
        mailSetData.stats.total = 100;
        this.component.attr.w = 20;
        this.component.attr.numPages = 0;

        this.component.trigger(Pixelated.events.ui.mails.fetchByTag, {tag: 'another tag'});

        g(mailSetData);
        expect(this.component.attr.numPages).toBe(5);
      });

      it('should have 6 pages with a 101 results and w 20', function() {
        mailSetData.stats.total = 101;
        this.component.attr.w = 20;
        this.component.attr.numPages = 0;

        this.component.trigger(Pixelated.events.ui.mails.fetchByTag, {tag: 'another tag'});

        g(mailSetData);
        expect(this.component.attr.numPages).toBe(6);
      });
    });

  });
});
