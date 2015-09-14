describeComponent('page/feedback', function () {
  'use strict';

  describe('feedback link', function () {

    it('should trigger ui:feedback:open event on click', function () {

      this.setupComponent('<nav id="feedback"></nav>', {});
      var spy = spyOnEvent(document, Pixelated.events.ui.feedback.open);

      this.$node.find('a').click();
      expect(spy).toHaveBeenTriggeredOn(document);
    });

  });
});

