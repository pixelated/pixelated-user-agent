/* global Pixelated */

describeComponent('user_alerts/ui/user_alerts', function () {
  'use strict';

  beforeEach(function () {
    setupComponent('<div id="userAlerts"></div>', { dismissTimeout: 100 });
  });

  it('should render message when ui:user_alerts:displayMessage is triggered', function () {
    this.component.trigger(Pixelated.events.ui.userAlerts.displayMessage, { message: 'a message' });

    expect(this.component.$node.html()).toMatch('a message');
  });

  it('should be emptied and hidden when hide is called', function() {
    expect(this.$node).not.toBeHidden();
    this.component.hide();
    expect(this.$node).toBeHidden();
    expect(this.$node.html()).toEqual('');
  });



});
