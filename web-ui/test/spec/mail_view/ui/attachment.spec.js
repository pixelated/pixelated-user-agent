describeComponent('mail_view/ui/attachment', function () {
  'use strict';

  describe('attachment', function () {
    beforeEach(function () {
        Pixelated.mockBloodhound();
        this.setupComponent();
    });

    it('render attachment button if feature enabled', function () {
        expect(this.$node.html()).toMatch('<i class="fa fa-paperclip fa-2x"></i>');
    });

    xit('uploads attachment on click', function () {
        var fileUploads = spyOn($, 'fileupload');
        this.$node.click();
        expect(fileUploads).toHaveBeenCalled();
    });

  });
});
