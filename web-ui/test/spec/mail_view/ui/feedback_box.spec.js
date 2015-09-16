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

});
