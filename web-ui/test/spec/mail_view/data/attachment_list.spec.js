describeMixin('mail_view/data/attachment_list', function () {
  'use strict';

    describe('initialization', function() {
        beforeEach(function(){
            this.setupComponent();
        });

        it('should add attachment to the list based on uploadedAttachment event', function () {
            var stubAttachment = {attachment_id: 'faked'};
            $(document).trigger(Pixelated.events.mail.appendAttachment, stubAttachment);
            expect(this.component.attr.attachments).toEqual([stubAttachment]);

            var anotherStubAttachment = {attachment_id: 'faked 2'};
            $(document).trigger(Pixelated.events.mail.appendAttachment, anotherStubAttachment);
            expect(this.component.attr.attachments).toEqual([stubAttachment, anotherStubAttachment]);
        });

    });

});
