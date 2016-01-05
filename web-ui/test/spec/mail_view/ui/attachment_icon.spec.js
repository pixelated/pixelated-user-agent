describeComponent('mail_view/ui/attachment_icon', function () {
  'use strict';

  describe('attachment', function () {
    beforeEach(function () {
        Pixelated.mockBloodhound();
        this.setupComponent();
    });

    it('should render attachment button if feature enabled', function () {
        expect(this.$node.html()).toMatch('<i class="fa fa-paperclip fa-2x"></i>');
    });

    it('should trigger starts of attachment upload process', function () {
        var triggerUploadAttachment = spyOnEvent(document, Pixelated.events.mail.startUploadAttachment);
        this.$node.click();
        expect(triggerUploadAttachment).toHaveBeenTriggeredOn(document);
    });

  });
});
