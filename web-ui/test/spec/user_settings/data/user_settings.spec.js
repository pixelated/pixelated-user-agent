describeComponent('user_settings/data/user_settings', function () {
  'use strict';

  beforeEach(function () {
    this.setupComponent();
  });

  it('gets user info from the server', function() {
    var data = {account_email: 'user@pixelated.org'};
    var deferred = $.Deferred();

    spyOn($, 'ajax').and.returnValue(deferred);
    this.component.getUserSettings();
    deferred.resolve();

    expect($.ajax.calls.mostRecent().args[0]).toEqual('/user-settings');
    expect($.ajax.calls.mostRecent().args[1].type).toEqual('GET');
  });

  it('send user info when event userSettings.getInfo is trigged', function() {
    var data = {account_email: 'user@pixelated.org'};
    var eventSpy = spyOnEvent(document, Pixelated.events.userSettings.here);
    
    this.component.trigger(document, Pixelated.events.userSettings.getInfo);

    expect(eventSpy).toHaveBeenTriggeredOn(document);
  });
});
