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
                this.$node.html('<i class="fa fa-paperclip"></i>');
            };

            this.triggerUploadAttachment = function () {
                this.trigger(document, events.mail.startUploadAttachment);
            };

            this.uploadInProgress = function (ev, data) {
                this.attr.busy = true;
                this.$node.addClass('busy');
            };

            this.uploadFinished = function (ev, data) {
                this.attr.busy = false;
                this.$node.removeClass('busy');
            };

            this.after('initialize', function () {
                if (features.isEnabled('attachment')) {
                    this.render();
                    this.on(document, events.mail.uploadingAttachment, this.uploadInProgress);
                    this.on(document, events.mail.uploadedAttachment, this.uploadFinished);
                    this.on(document, events.mail.failedUploadAttachment, this.uploadFinished);
                }
                this.on(this.$node, 'click', function() {
                    if (!this.attr.busy) {
                        this.triggerUploadAttachment();
                    }
                });
            });
        });
    });
