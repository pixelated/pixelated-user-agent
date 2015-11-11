describeComponent('dispatchers/middle_pane_dispatcher', function () {
  'use strict';

  beforeEach(function() {
    this.setupComponent('<div><div id="middle-pane" style="height: 200px; overflow-y: scroll;"><div style="height: 400px"></div></div></div>');
  });

  it ('listens to refresh mail list event', function() {
    var mailsListRefreshEventSpy = spyOnEvent(document, Pixelated.events.ui.mails.fetchByTag);
    this.component.trigger(document, Pixelated.events.dispatchers.middlePane.refreshMailList);
    expect(mailsListRefreshEventSpy).toHaveBeenTriggeredOn(document);
  });

  it ('listens to unselect event', function() {
    var mailListUnselectEvent = spyOnEvent(document, Pixelated.events.ui.mails.cleanSelected);
    this.component.trigger(document, Pixelated.events.dispatchers.middlePane.cleanSelected);
    expect(mailListUnselectEvent).toHaveBeenTriggeredOn(document);
  });

  it('resets the scrollTop value when asked to', function() {
    this.component.select('middlePane').scrollTop(200);
    this.component.trigger(document, Pixelated.events.dispatchers.middlePane.resetScroll);
    expect(this.component.select('middlePane').scrollTop()).toEqual(0);
  });

  describe('no emails available', function () {
    var noMailsAvailablePane, attachToSpy;
    beforeEach(function () {
      noMailsAvailablePane = require('mail_view/ui/no_mails_available_pane');
      attachToSpy = spyOn(noMailsAvailablePane, 'attachTo');
      spyOn(noMailsAvailablePane, 'teardownAll');
    });

    it('should listen to mails available event and show noMailsAvailablePane', function () {
        var mail_list = { mails: []};
        this.component.trigger(document, Pixelated.events.mails.available, mail_list);

        expect(noMailsAvailablePane.attachTo).toHaveBeenCalled();
    });

    it('should listen to mails available event and do not show noMailsAvailablePane', function () {
        var pretend_to_be_a_mail = {};
        var mail_list = { mails: [pretend_to_be_a_mail]};
        this.component.trigger(document, Pixelated.events.mails.available, mail_list);

        expect(noMailsAvailablePane.attachTo).not.toHaveBeenCalled();
        expect(noMailsAvailablePane.teardownAll).toHaveBeenCalled();
    });

    it('should give search information to component', function () {
        var mail_list = { mails: [], tag: 'all', forSearch: 'search'};
        this.component.trigger(document, Pixelated.events.mails.available, mail_list);
 
        expect(attachToSpy.calls.mostRecent().args[1]).toEqual({tag: 'all', forSearch: 'search'});
    });
  });
});
