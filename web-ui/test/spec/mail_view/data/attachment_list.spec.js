describeComponent('mail_view/data/attachment_list', function () {
    'use strict';

    describe('initialization', function () {
        beforeEach(function () {
            this.setupComponent('<div id="attachment-list">' +
                '<ul><li id="attachment-list-item"> </li></ul>' +
                '</div>');
        });

        it('should add attachment to the list based on uploadedAttachment event', function () {
            var stubAttachment = {attachment_id: 'faked'};
            $(document).trigger(Pixelated.events.mail.uploadedAttachment, stubAttachment);
            expect(this.component.attr.attachments).toEqual([stubAttachment]);

            var anotherStubAttachment = {attachment_id: 'faked 2'};
            $(document).trigger(Pixelated.events.mail.uploadedAttachment, anotherStubAttachment);
            expect(this.component.attr.attachments).toEqual([stubAttachment, anotherStubAttachment]);
        });

        it('should render attachment list view based on uploadedAttachment event', function () {
            var stubAttachment = {attachment_id: 'faked', filename: 'haha.txt', filesize: 4500};

            $(document).trigger(Pixelated.events.mail.uploadedAttachment, stubAttachment);

            var expected_li = '<a href="/attachment/faked?filename=haha.txt&amp;encoding=base64">haha.txt (4.39 Kb)</a>';
            expect(this.component.select('attachmentListItem').html()).toEqual(expected_li);
        });

        xit('should start uploading attachments', function () {
            var stubAttachment = {attachment_id: 'faked', filename: 'haha.txt', filesize: 4500};
            var mockAjax = spyOn($, 'ajax').and.callFake(function (params) {params.success(stubAttachment);});
            var uploadedAttachment = spyOnEvent(document, Pixelated.events.mail.uploadedAttachment);
            var uploading = spyOnEvent(document, Pixelated.events.mail.uploadingAttachment);

            $(document).trigger(Pixelated.events.mail.startUploadAttachment);

            expect(mockAjax).toHaveBeenCalled();
            expect(uploadedAttachment).toHaveBeenTriggeredOnAndWith(document, stubAttachment);
            expect(uploading).toHaveBeenTriggeredOn(document);
        });

    });

});
