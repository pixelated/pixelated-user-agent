describeComponent('services/mail_service', function () {
  'use strict';
  var email1, i18n;
  var features;

  beforeEach( function () {
    features = require('features');
    spyOn(features, 'isAutoRefreshEnabled').and.returnValue(false);
    this.setupComponent();

    email1 = Pixelated.testData().parsedMail.simpleTextPlain;
    i18n = require('views/i18n');
  } );

  it('marks the desired message as read', function () {
    var deferred = $.Deferred();
    var readRequest = spyOn($, 'ajax').and.returnValue(deferred);

    this.component.trigger(Pixelated.events.mail.read, {ident: 1});

    expect(readRequest.calls.mostRecent().args[0]).toEqual('/mails/read');
    expect(readRequest.calls.mostRecent().args[1].data).toEqual('{"idents":[1]}');
  });

  describe('when marks many emails as read', function () {
    var readRequest, checkedMails, uncheckAllEvent, deferred;

    beforeEach(function () {
      checkedMails = {
        1: {ident: 1},
        2: {ident: 2}
      };

      deferred = $.Deferred();
      readRequest = spyOn($, 'ajax').and.returnValue(deferred);

      uncheckAllEvent = spyOnEvent(document, Pixelated.events.ui.mails.uncheckAll);
      spyOn(this.component, 'refreshMails');

      this.component.trigger(Pixelated.events.mail.read, {checkedMails: checkedMails});
    });

    it('makes the correct request to the backend', function () {
      expect(readRequest.calls.mostRecent().args[0]).toEqual('/mails/read');
      expect(readRequest.calls.mostRecent().args[1].data).toEqual('{"idents":[1,2]}');
    });

    it('will trigger that a message has been deleted when it is done deleting', function() {
      deferred.resolve(checkedMails);
      expect(this.component.refreshMails).toHaveBeenCalled();
    });

    it('clears the check all checkbox', function () {
      deferred.resolve(checkedMails);
      expect(uncheckAllEvent).toHaveBeenTriggeredOn(document);
    });
  });

  it('fetches a single email', function () {
    var me = {};
    var deferred = $.Deferred();
    var spyAjax = spyOn($, 'ajax').and.returnValue(deferred);
    var mailHereEvent = spyOnEvent(me, Pixelated.events.mail.here);

    this.component.trigger(Pixelated.events.mail.want, { caller: me, mail: email1.ident });

    deferred.resolve();

    expect(mailHereEvent).toHaveBeenTriggeredOn(me);
    expect(spyAjax.calls.mostRecent().args[0]).toEqual('/mail/' + email1.ident);
  });

  it('answers mail:notFound if mail returned from server is null', function () {
    var me = {};
    var deferred = $.Deferred();
    var spyAjax = spyOn($, 'ajax').and.returnValue(deferred);
    var mailNotFound = spyOnEvent(me, Pixelated.events.mail.notFound);

    this.component.trigger(Pixelated.events.mail.want, { caller: me, mail: email1.ident });

    deferred.resolve(null);

    expect(mailNotFound).toHaveBeenTriggeredOn(me);
  });

  it('updates the tags of the desired message', function () {
    spyOn(this.component, 'refreshMails');
    var tagListRefreshEvent = spyOnEvent(document, Pixelated.events.dispatchers.tags.refreshTagList);
    var updateTagsReturnValue = { tags: ['website'], mailbox: 'inbox'};
    var deferred = $.Deferred();
    var spyAjax = spyOn($, 'ajax').and.returnValue(deferred);

    var spyEvent = spyOnEvent(document, Pixelated.events.mail.tags.updated);

    this.component.trigger(Pixelated.events.mail.tags.update, { ident: email1.ident, tags: email1.tags });

    deferred.resolve(updateTagsReturnValue);

    expect(spyEvent).toHaveBeenTriggeredOn(document);
    expect(spyAjax.calls.all()[0].args[0]).toEqual('/mail/1/tags');
    expect(spyAjax.calls.all()[0].args[1].data).toEqual(JSON.stringify({ newtags: email1.tags } ));
    expect(this.component.refreshMails).toHaveBeenCalled();
    expect(tagListRefreshEvent).toHaveBeenTriggeredOn(document);
  });

  it('triggers an error message when it can\'t update the tags', function () {
    var deferred = $.Deferred();
    var spyAjax = spyOn($, 'ajax').and.returnValue(deferred);

    var spyEvent = spyOnEvent(document, Pixelated.events.ui.userAlerts.displayMessage);

    this.component.trigger(Pixelated.events.mail.tags.update, { ident: email1.ident, tags: email1.tags });

    deferred.reject({}, 500);

    expect(spyEvent).toHaveBeenTriggeredOn(document);
    expect(spyAjax.calls.mostRecent().args[0]).toEqual('/mail/1/tags');
    expect(spyAjax.calls.mostRecent().args[1].data).toEqual(JSON.stringify({ newtags: email1.tags } ));
  });

  it('will try to delete a message when requested to', function() {
    var spyAjax = spyOn($, 'ajax').and.returnValue($.Deferred());
    this.component.trigger(Pixelated.events.mail.delete, {mail: {ident: '43'}});
    expect(spyAjax).toHaveBeenCalled();
    expect(spyAjax.calls.mostRecent().args[0]).toEqual('/mail/43');
    expect(spyAjax.calls.mostRecent().args[1].type).toEqual('DELETE');
  });

  describe('when successfuly deletes an email', function () {
    var displayMessageEvent, uncheckAllEvent, mailsDeletedEvent;

    beforeEach(function () {
      displayMessageEvent = spyOnEvent(document, Pixelated.events.ui.userAlerts.displayMessage);
      uncheckAllEvent = spyOnEvent(document, Pixelated.events.ui.mails.uncheckAll);
      mailsDeletedEvent = spyOnEvent(document, Pixelated.events.mail.deleted);
      spyOn(this.component, 'refreshMails');

      this.component.triggerDeleted({
        successMessage: 'A success message',
        mails: {1: 'email 1', 2: 'email 2'}
      })();
    });

    it('will trigger that a message has been deleted when it is done deleting', function() {
      expect(this.component.refreshMails).toHaveBeenCalled();
    });

    it('displays a success message', function () {
      expect(displayMessageEvent).toHaveBeenTriggeredOnAndWith(document, {message: 'A success message'});
    });

    it('tells about deleted emails', function () {
      expect(mailsDeletedEvent).toHaveBeenTriggeredOnAndWith(document, { mails: {1: 'email 1', 2: 'email 2'} });
    });

    it('unchecks all checked mails', function () {
      expect(uncheckAllEvent).toHaveBeenTriggeredOn(document);
    });
  });

  it('will trigger an error message when a message cannot be deleted', function() {
    var deferred = $.Deferred();
    spyOn($, 'ajax').and.returnValue(deferred);
    var spyEvent = spyOnEvent(document, Pixelated.events.ui.userAlerts.displayMessage);

    this.component.trigger(Pixelated.events.mail.delete, {mail: {ident: '43'}});

    deferred.reject({mailsJSON: {}});

    expect(spyEvent).toHaveBeenTriggeredOnAndWith(document, {message: i18n.t('Could not delete email')} );
  });

  it('will try to recover a message when requested to', function() {
    var spyAjax = spyOn($, 'ajax').and.returnValue($.Deferred());
    this.component.trigger(Pixelated.events.mail.recoverMany, {mails: [{ident: '43'}, {ident: '44'}]});
    expect(spyAjax).toHaveBeenCalled();
    expect(spyAjax.calls.mostRecent().args[0]).toEqual('/mails/recover');
    expect(spyAjax.calls.mostRecent().args[1].type).toEqual('POST');
    expect(spyAjax.calls.all()[0].args[1].data).toEqual(JSON.stringify({ idents: ['43', '44'] } ));
  });

  // TODO: WIP
  describe('when try archive emails', function() {
    var deferred, spyAjax, mails;

    beforeEach(function() {
      deferred = $.Deferred();
      spyAjax = spyOn($, 'ajax').and.returnValue(deferred);
      mails = {checkedMails: [{ident: '43'}, {ident: '44'}]};
    });

    it('should call triggerArchived', function() {
      spyOn(this.component, 'triggerArchived');

      this.component.trigger(Pixelated.events.mail.archiveMany, mails);

      deferred.resolve();
      expect(this.component.triggerArchived).toHaveBeenCalledWith(mails);
    });

    it('should show an error message when request returns no success', function() {
      spyOn(this.component, 'errorMessage');

      this.component.trigger(Pixelated.events.mail.archiveMany, mails);

      deferred.reject({});
      expect(this.component.errorMessage).toHaveBeenCalledWith(i18n.t('could-not-archive'));
    });

    it('make an ajax request to /mails/archive', function() {
      this.component.trigger(Pixelated.events.mail.archiveMany,
                            {checkedMails: [{ident: '43'}, {ident: '44'}]});

      expect(spyAjax).toHaveBeenCalled();
      expect(spyAjax.calls.mostRecent().args[0]).toEqual('/mails/archive');
      expect(spyAjax.calls.mostRecent().args[1].type).toEqual('POST');
      expect(spyAjax.calls.all()[0].args[1].data).toEqual(JSON.stringify({ idents: ['43', '44'] } ));
    });
  });

  describe('when successfuly recovers emails', function () {
    var displayMessageEvent, uncheckAllEvent, mailsRecoveredEvent;

    beforeEach(function () {
      displayMessageEvent = spyOnEvent(document, Pixelated.events.ui.userAlerts.displayMessage);
      uncheckAllEvent = spyOnEvent(document, Pixelated.events.ui.mails.uncheckAll);
      spyOn(this.component, 'refreshMails');

      this.component.triggerRecovered({
        successMessage: 'A success message',
        mails: {1: 'email 1', 2: 'email 2'}
      })();
    });

    it('will trigger that a message has been recovered when it is done recovering', function() {
      expect(this.component.refreshMails).toHaveBeenCalled();
    });

    it('displays a success message', function () {
      expect(displayMessageEvent).toHaveBeenTriggeredOnAndWith(document, {message: 'A success message'});
    });

    it('unchecks all checked mails', function () {
      expect(uncheckAllEvent).toHaveBeenTriggeredOn(document);
    });
  });

  it('triggers mails:available with received mails and keeps that tag as the current tag', function() {
    var eventSpy = spyOnEvent(document, Pixelated.events.mails.available);

    var deferred = $.Deferred();
    var spyAjax = spyOn($, 'ajax').and.returnValue(deferred);
    this.component.trigger(Pixelated.events.ui.tag.selected, {tag: 'inbox'});

    deferred.resolve({stats: {}, mails: [email1]});

    expect(eventSpy.mostRecentCall.data.stats).toEqual({});
    expect(eventSpy.mostRecentCall.data.tag).toEqual('inbox');
    expect(this.component.attr.currentTag).toEqual('inbox');
  });

  it('wraps the tag in quotes before fetching by tag (to support tags with spaces)', function () {
    spyOn($, 'ajax').and.returnValue($.Deferred());

    this.component.trigger(Pixelated.events.ui.tag.selected, {tag: 'new tag'});

    expect($.ajax.calls.mostRecent().args[0]).toContain(encodeURIComponent('tag:"new tag"'));
  });

  describe('pagination', function() {
    var pageChangedEvent;
    var deferred;

    beforeEach(function () {
      pageChangedEvent = spyOnEvent(document, Pixelated.events.ui.page.changed);
      deferred = $.Deferred();
      var spyAjax = spyOn($, 'ajax').and.returnValue(deferred);
      spyOn(this.component, 'refreshMails').and.callThrough();
    });

    it('changes to the previous page and refetch email when ui:page:previous is fired', function() {
      this.component.attr.currentPage = 2;

      this.component.trigger(Pixelated.events.ui.page.previous);

      expect(this.component.refreshMails).toHaveBeenCalled();
      expect(this.component.attr.currentPage).toEqual(1);
    });

    it('won\'t change the page if it was already at the first page and trying to go to previous', function() {
      this.component.attr.currentPage = 1;

      this.component.trigger(Pixelated.events.ui.page.previous);

      expect(this.component.refreshMails).not.toHaveBeenCalled();
      expect(this.component.attr.currentPage).toEqual(1);
    });

    it('changes to the next page and refetch email when ui:page:next is fired', function() {
      this.component.attr.numPages = 10;
      this.component.attr.currentPage = 1;

      this.component.trigger(Pixelated.events.ui.page.next);

      expect(this.component.refreshMails).toHaveBeenCalled();
      expect(this.component.attr.currentPage).toEqual(2);
    });

    it('won\'t change the page if it is at the last mail when ui:page:next is fired', function() {
      this.component.attr.numPages = 9;
      this.component.attr.currentPage = 9;

      this.component.trigger(Pixelated.events.ui.page.next);

      expect(this.component.refreshMails).not.toHaveBeenCalled();
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
      this.component.trigger(Pixelated.events.ui.tag.selected, {tag: 'inbox'});

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
        this.component.attr.pageSize = 20;
        this.component.attr.numPages = 0;

        this.component.trigger(Pixelated.events.ui.tag.selected, {tag: 'another tag'});

        deferred.resolve(mailSetData);
        expect(this.component.attr.numPages).toBe(5);
      });

      it('should have 6 pages with a 101 results and w 20', function() {
        mailSetData.stats.total = 101;
        this.component.attr.pageSize = 20;
        this.component.attr.numPages = 0;

        this.component.trigger(Pixelated.events.ui.tag.selected, {tag: 'another tag'});

        deferred.resolve(mailSetData);
        expect(this.component.attr.numPages).toBe(6);
      });
    });

  });
});
