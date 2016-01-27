/*
 * Copyright (c) 2015 ThoughtWorks, Inc.
 *
 * Pixelated is free software: you can redistribute it and/or modify
 * it under the terms of the GNU Affero General Public License as published by
 * the Free Software Foundation, either version 3 of the License, or
 * (at your option) any later version.
 *
 * Pixelated is distributed in the hope that it will be useful,
 * but WITHOUT ANY WARRANTY; without even the implied warranty of
 * MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
 * GNU Affero General Public License for more details.
 *
 * You should have received a copy of the GNU Affero General Public License
 * along with Pixelated. If not, see <http://www.gnu.org/licenses/>.
 */

define(
    [
        'views/templates',
        'page/events',
        'helpers/view_helper'
    ],

    function (templates, events, viewHelper) {
        'use strict';

        function attachmentList() {
            this.defaultAttrs({
                inputFileUpload: '#fileupload',
                attachmentListItem: '#attachment-list-item',
                progressBar: '#progress .progress-bar',
                attachmentBaseUrl: '/attachment',
                attachments: [],
                closeIcon: '.close-icon',
                uploadError: '#upload-error',
                dismissButton: '#dismiss-button',
                uploadFileButton: '#upload-file-button'
            });

            this.showAttachment = function (ev, data) {
                this.trigger(document, events.mail.appendAttachment, data);
                this.renderAttachmentListView(data);
            };

            this.addAttachment = function (event, data) {
                this.attr.attachments.push(data);
            };

            this.renderAttachmentListView = function (data) {
                var currentHtml = this.select('attachmentListItem').html();
                var item = this.buildAttachmentListItem(data);
                this.select('attachmentListItem').html(currentHtml + item);
            };

            this.buildAttachmentListItem = function (attachment) {
                var attachmentData = {ident: attachment.ident,
                                      encoding: attachment.encoding,
                                      name: attachment.name,
                                      size: attachment.size};
                return templates.compose.attachmentItem(attachmentData);
            };

            this.addJqueryFileUploadConfig = function() {
                var self = this;
                this.select('inputFileUpload').fileupload({
                    add: function(e, data) {
                        var uploadError = self.select('uploadError');
                        if (uploadError) {
                            uploadError.remove();
                        }

                        var uploadErrors = [];

                        this.showUploadFailed = function () {
                            var html = $(templates.compose.uploadAttachmentFailed());
                            html.insertAfter(self.$node.find(self.attr.attachmentListItem));

                            self.on(self.select('closeIcon'), 'click', this.dismissUploadFailed);
                            self.on(self.select('dismissButton'), 'click', this.dismissUploadFailed);
                            self.on(self.select('uploadFileButton'), 'click', this.uploadAnotherFile);
                        };

                        this.dismissUploadFailed = function (event) {
                            event.preventDefault();
                            self.select('uploadError').remove();
                        };

                        this.uploadAnotherFile = function (event) {
                            event.preventDefault();
                            self.startUpload();
                        };

                        if(data.originalFiles[0].size > 1000000) {
                            uploadErrors.push('Filesize is too big');
                        }
                        if(uploadErrors.length > 0) {
                            this.showUploadFailed();
                        } else {
                            data.submit();
                        }
                    },
                    url: self.attr.attachmentBaseUrl,
                    dataType: 'json',
                    done: function (e, response) {
                        var data = response.result;
                        self.trigger(document, events.mail.uploadedAttachment, data);
                    },
                    progressall: function (e, data) {
                        var progressRate = parseInt(data.loaded / data.total * 100, 10);
                        self.select('progressBar').css('width', progressRate + '%');
                    }
                }).bind('fileuploadstart', function (e) {
                    self.trigger(document, events.mail.uploadingAttachment);
                }).bind('fileuploadadd', function (e) {
                    $('.attachmentsAreaWrap').show();
                });
            };

            this.startUpload = function () {
                this.addJqueryFileUploadConfig();
                this.select('inputFileUpload').click();
            };

            this.after('initialize', function () {
                this.addJqueryFileUploadConfig();
                this.on(document, events.mail.uploadedAttachment, this.showAttachment);
                this.on(document, events.mail.startUploadAttachment, this.startUpload);
                this.on(document, events.mail.appendAttachment, this.addAttachment);
            });
        }

        return attachmentList;
    });
