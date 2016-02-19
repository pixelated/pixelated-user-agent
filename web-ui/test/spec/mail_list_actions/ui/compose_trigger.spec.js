describeComponent('mail_list_actions/ui/compose_trigger', function () {
  'use strict';

  beforeEach(function () {
    this.setupComponent('<div></div>');
  });

  it('triggers the enableComposebox event when clicked', function () {
    var spyEvent = spyOnEvent(document, Pixelated.events.dispatchers.rightPane.openComposeBox);

    this.component.trigger('click');

    expect(spyEvent).toHaveBeenTriggeredOn(document);
  });

  it('trigger showEmailSuccess message when message is sent', function () {
      var spyEvent = spyOnEvent(document, Pixelated.events.ui.userAlerts.displayMessage);

      this.component.trigger(document, Pixelated.events.mail.sent);

      expect(spyEvent).toHaveBeenTriggeredOnAndWith(document, {message: 'Your message was sent!', class: 'success'});
  });

  it('trigger showEmailError message when message is not sent', function () {
      var spyEvent = spyOnEvent(document, Pixelated.events.ui.userAlerts.displayMessage);

      this.component.trigger(document, Pixelated.events.mail.send_failed, {responseJSON: {message: 'failure'}});

      expect(spyEvent).toHaveBeenTriggeredOnAndWith(document, {message: 'Error,  message not sent: failure', class: 'error'});
  });
});
