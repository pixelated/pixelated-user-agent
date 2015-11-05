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
    var noMailsAvailablePane;
    beforeEach(function () {
      noMailsAvailablePane = require('mail_view/ui/no_mails_available_pane');
      spyOn(noMailsAvailablePane, 'attachTo');
      spyOn(noMailsAvailablePane, 'teardownAll');
    });

    it('should listen to no mails available event and show noMailsAvailablePane', function () {
        var mail_list = { mails: []};
        this.component.trigger(document, Pixelated.events.mails.available, mail_list);

        expect(noMailsAvailablePane.attachTo).toHaveBeenCalled();
    });

    it('should tbd', function () {
        var pretend_to_be_a_mail = {};
        var mail_list = { mails: [pretend_to_be_a_mail]};
        this.component.trigger(document, Pixelated.events.mails.available, mail_list);

        expect(noMailsAvailablePane.attachTo).not.toHaveBeenCalled();
        expect(noMailsAvailablePane.teardownAll).toHaveBeenCalled();
    });

  });
});
