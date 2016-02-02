describeComponent('mail_view/ui/attachment_icon', function () {
  'use strict';

  describe('attachment', function () {
    beforeEach(function () {
        Pixelated.mockBloodhound();
        this.setupComponent();
    });

    it('should render attachment button if feature enabled', function () {
        expect(this.$node.html()).toMatch('<i class="fa fa-paperclip"></i>');
    });

    it('should be busy', function() {
        this.component.uploadInProgress();

        expect(this.component.attr.busy).toBe(true);
    });

    it('should not be busy', function() {
        this.component.uploadFinished();

        expect(this.component.attr.busy).toBe(false);
    });

    it('should trigger start of attachment upload process', function () {
        var triggerUploadAttachment = spyOnEvent(document, Pixelated.events.mail.startUploadAttachment);

        this.$node.click();

        expect(triggerUploadAttachment).toHaveBeenTriggeredOn(document);
    });

    it('should not trigger attachment upload when busy', function () {
        this.component.uploadInProgress();
        var triggerUploadAttachment = spyOnEvent(document, Pixelated.events.mail.startUploadAttachment);

        this.$node.click();

        expect(triggerUploadAttachment).not.toHaveBeenTriggeredOn(document);
    });

  });
});
