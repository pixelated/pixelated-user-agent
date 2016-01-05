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

        it('should reset attachment list on compose', function () {
            this.component.attr.attachments = ['some array'];
            $(document).trigger(Pixelated.events.mail.resetAttachments);

            expect(this.component.attr.attachments).toEqual([]);
        });

        it('should reset attachment list and tear down when email sent', function () {
            this.component.attr.attachments = ['some array'];
            $(document).trigger(Pixelated.events.mail.sent);

            expect(this.component.attr.attachments).toEqual([]);
        });

    });

});
