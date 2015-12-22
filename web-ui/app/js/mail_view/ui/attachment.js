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
        'flight/lib/component',
        'page/events',
        'features'
    ],

    function (defineComponent, events, features) {
        'use strict';

        return defineComponent(function () {
            this.render = function () {
                this.$node.html('<i class="fa fa-paperclip fa-2x"></i>');
            };

            function humanReadable(bytes) {
                var e = Math.floor(Math.log(bytes) / Math.log(1024));
                return (bytes / Math.pow(1024, e)).toFixed(2) + ' ' + ' KMGTP'.charAt(e) + 'b';
            }

            function addJqueryFileUploadConfig(on) {
                var url = '/attachment';
                $('#fileupload').fileupload({
                    url: url,
                    dataType: 'json',
                    done: function (e, response) {
                        var data = response.result;
                        $('#files').html('<span>' + data.filename + ' (' + humanReadable(data.filesize) + ')' + '</span>');
                        on.trigger(document, events.mail.uploadedAttachment, data);
                    },
                    progressall: function (e, data) {
                        var progress = parseInt(data.loaded / data.total * 100, 10);
                        $('#progress .progress-bar').css('width', progress + '%');
                    }
                });
            }

            this.upload = function () {
                addJqueryFileUploadConfig(this);
                $('#fileupload').click();
            };

            this.after('initialize', function () {
                if (features.isEnabled('attachment')) {
                    this.render();
                }
                this.on(this.$node, 'click', this.upload);
            });

        });
    });
