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

            expect(this.component.select('attachmentListItem').html()).toContain('href="/attachment/faked');
            expect(this.component.select('attachmentListItem').html()).toContain('filename=haha.txt');
            expect(this.component.select('attachmentListItem').html()).toContain('encoding=base64');
            expect(this.component.select('attachmentListItem').html()).toContain('haha.txt');
            expect(this.component.select('attachmentListItem').html()).toContain('(4.39 Kb');
        });

        describe('Upload files -- max file size -- ', function (){
            var submitFile = 'file not submitted', submitted = 'file submitted';
            var mockSubmit = function (){ submitFile = submitted; };
            var largeAttachment = {originalFiles: [{size: 4500000}], submit: mockSubmit};
            var dummyEvent = 'whatever, not used';

            it('should show error messages on the dom, when uploading files larger than 1MB', function () {
                this.component.checkAttachmentSize(dummyEvent, largeAttachment);

                expect(this.component.select('uploadError').html()).toContain('Upload failed. This file exceeds the 1MB limit.');
            });

            xit('should dismiss upload failed message when clicking close icon', function () {

            });

            it('should not upload files larger than 1MB', function () {
                spyOn(largeAttachment, 'submit');

                this.component.checkAttachmentSize(dummyEvent, largeAttachment);

                expect(largeAttachment.submit).not.toHaveBeenCalled();
            });

            it('should upload files smaller than 1MB', function () {
                var smallAttachment = {originalFiles: [{size: 450}], submit: mockSubmit};
                this.component.checkAttachmentSize(dummyEvent, smallAttachment);

                expect(submitFile).toEqual(submitted);
            });
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
