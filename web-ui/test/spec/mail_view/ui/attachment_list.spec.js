describeMixin('mail_view/ui/attachment_list', function () {
    'use strict';

    describe('initialization', function () {
        beforeEach(function () {
            this.setupComponent('<div id="attachment-list">' +
                '<ul id="attachment-list-item"></ul>' +
                '</div>');
        });

        it('should add attachment to the list based on uploadedAttachment event', function () {
            var stubAttachment = {ident: 'faked'};
            $(document).trigger(Pixelated.events.mail.appendAttachment, stubAttachment);
            expect(this.component.attr.attachments).toEqual([stubAttachment]);

            var anotherStubAttachment = {ident: 'faked 2'};
            $(document).trigger(Pixelated.events.mail.appendAttachment, anotherStubAttachment);
            expect(this.component.attr.attachments).toEqual([stubAttachment, anotherStubAttachment]);
        });

        it('should trigger add attachment event', function () {
            var triggerUploadAttachment = spyOnEvent(document, Pixelated.events.mail.appendAttachment);
            var stubAttachment = {ident: 'faked'};

            $(document).trigger(Pixelated.events.mail.uploadedAttachment, stubAttachment);

            expect(triggerUploadAttachment).toHaveBeenTriggeredOnAndWith(document, stubAttachment);
        });

        it('should render attachment list view based on uploadedAttachment event', function () {
            var stubAttachment = {ident: 'faked', name: 'haha.txt', size: 4500, encoding: 'base64'};

            $(document).trigger(Pixelated.events.mail.uploadedAttachment, stubAttachment);

            var expected_li = '<li><a href="/attachment/faked?filename=haha.txt&amp;encoding=base64">haha.txt <span class="attachment-size"> (4.39 Kb)</span></a></li>';
            expect(this.component.select('attachmentListItem').html()).toEqual(expected_li);
        });

        xit('should start uploading attachments', function () {
            var stubAttachment = {ident: 'faked', name: 'haha.txt', size: 4500};
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
