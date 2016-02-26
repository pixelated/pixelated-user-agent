describeComponent('user_alerts/ui/user_alerts', function () {
  'use strict';

  beforeEach(function () {
    this.setupComponent('<div id="userAlerts"></div>', { dismissTimeout: 100 });
  });

  it('should render message when ui:user_alerts:displayMessage is triggered', function () {
    this.component.trigger(Pixelated.events.ui.userAlerts.displayMessage, { message: 'a message' });

    expect(this.component.$node.html()).toEqual('<span class="success">a message</span>\n');
  });

  it('should render error message', function () {
    this.component.trigger(Pixelated.events.ui.userAlerts.displayMessage, { message: 'send failed', class: 'error' });

    expect(this.component.$node.html()).toEqual('<span class="error">send failed</span>\n');
  });

  it('should be emptied and hidden when hide is called', function() {
    expect(this.$node).not.toBeHidden();
    this.component.hide();
    expect(this.$node).toBeHidden();
    expect(this.$node.html()).toEqual('');
  });



});
