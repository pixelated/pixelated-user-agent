describeComponent('mail_view/ui/feedback_box', function () {
  'use strict';
  beforeEach(function () {
    Pixelated.mockBloodhound();
    this.setupComponent('<div></div>');
  });


  describe('close button behavior', function() {

    it('should fire Show no message selected if the close button is clicked', function() {
      var spy = spyOnEvent(document, Pixelated.events.dispatchers.rightPane.openNoMessageSelected);
      this.component.select('closeButton').click();
      expect(spy).toHaveBeenTriggeredOn(document);
    });

  });

  describe('when submit feedback', function () {
    it('should display submitted message', function() {
      var spy = spyOnEvent(document, Pixelated.events.ui.userAlerts.displayMessage);
      this.component.select('submitButton').click();
      expect(spy).toHaveBeenTriggeredOnAndWith(document, { message: 'Thanks for your feedback!' });
    });

    it('should close feedback box after submit', function() {
      var spy = spyOnEvent(document, Pixelated.events.dispatchers.rightPane.openNoMessageSelected);
      this.component.select('submitButton').click();
      expect(spy).toHaveBeenTriggeredOn(document);
    });
  });

});
