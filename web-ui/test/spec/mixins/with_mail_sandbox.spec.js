describeMixin('mixins/with_mail_sandbox', function() {
  'use strict';

  beforeEach(function() {
    this.setupComponent();
  });

  it('should open reply container', function () {
    var showContainerEvent = spyOnEvent(document, Pixelated.events.ui.replyBox.showReplyContainer);
    this.component.showMailOnSandbox(Pixelated.testData().parsedMail.html);
    expect(showContainerEvent).toHaveBeenTriggeredOn(document);
  });

});
