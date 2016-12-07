/*
 * Copyright (c) 2014 ThoughtWorks, Inc.
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

define(['services/model/mail'], function (mailModel) {
    'use strict';

    var mail;

    function recipients(mail, place, v) {
        if (v !== '' && !_.isUndefined(v)) {
            if (_.isArray(v)) {
                mail[place] = v;
            } else {
                mail[place] = v.split(' ');
            }
        } else {
            mail[place] = [];
        }
    }

    return {
        newMail: function (ident) {
            ident = _.isUndefined(ident) ? '' : ident;

            mail = {
                header: {
                    to: [],
                    cc: [],
                    bcc: [],
                    from: undefined,
                    subject: ''
                },
                tags: [],
                body: '',
                attachments: [],
                ident: ident
            };
            return this;
        },

        subject: function (subject) {
            mail.header.subject = subject;
            return this;
        },

        body: function (body) {
            mail.body = body;
            return this;
        },

        to: function (to) {
            recipients(mail.header, 'to', to);
            return this;
        },

        cc: function (cc) {
            recipients(mail.header, 'cc', cc);
            return this;
        },

        bcc: function (bcc) {
            recipients(mail.header, 'bcc', bcc);
            return this;
        },

        header: function (name, value) {
            mail.header[name] = value;
            return this;
        },

        tag: function (tag) {
            if (_.isUndefined(tag)) {
                tag = 'drafts';
            }
            mail.tags.push(tag);
            return this;
        },

        attachment: function (attachmentList) {
            mail.attachments = attachmentList;
            return this;
        },

        build: function () {
            return mailModel.create(mail);
        }
    };
});
