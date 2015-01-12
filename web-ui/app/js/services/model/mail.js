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
'use strict';

define(['helpers/contenttype'],
  function (contentType) {

  var asMail = (function () {

    function isSentMail() {
      return this.mailbox === 'SENT';
    }

    function isDraftMail() {
      return  this.mailbox === 'DRAFTS';
    }

    function isInTrash() {
      return this.mailbox.toLowerCase() === 'trash';
    }

    function setDraftReplyFor(ident) {
      this.draft_reply_for = ident;
    }

    function replyToAddress() {
      return {
        to: [this.replying.single],
        cc: []
      };
    }

    function replyToAllAddress() {
      return {
        to: this.replying.all['to-field'],
        cc: this.replying.all['cc-field']
      };
    }

    function getHeadersFromMailPart (rawBody) {
      var lines, headerLines, endOfHeaders, headers;

      lines = rawBody.split('\n');
      endOfHeaders = _.indexOf(lines, '');
      headerLines = lines.slice(0, endOfHeaders);

      headers = _.map(headerLines, function (headerLine) {
        return _.map(headerLine.split(':'), function(elem){return elem.trim();});
      });

      return _.object(headers);
    }

    function getBodyFromMailPart (rawBody) {
      var lines, endOfHeaders;

      lines = rawBody.split('\n');
      endOfHeaders = _.indexOf(lines, '');

      return lines.slice(endOfHeaders + 1).join('\n');
    }

    function parseWithHeaders(rawBody) {
      return {headers: getHeadersFromMailPart(rawBody), body: getBodyFromMailPart(rawBody)};
    }

    function getMailMultiParts () {
      var mediaType = this.getMailMediaType();
      var boundary = '--' + mediaType.params.boundary + '\n';
      var finalBoundary = '--' + mediaType.params.boundary + '--';

      var bodyParts = this.body.split(finalBoundary)[0].split(boundary);

      bodyParts = _.reject(bodyParts, function(bodyPart) { return _.isEmpty(bodyPart.trim()); });

      return _.map(bodyParts, parseWithHeaders);
    }

    function getMailMediaType () {
      return new contentType.MediaType(this.header.content_type);
    }

    function isMailMultipartAlternative () {
      return this.getMailMediaType().type === 'multipart/alternative';
    }

    function availableBodyPartsContentType () {
      var bodyParts = this.getMailMultiParts();

      return _.pluck(_.pluck(bodyParts, 'headers'), 'Content-Type');
    }

    function getMailPartByContentType (contentType) {
      var bodyParts = this.getMailMultiParts();

      return _.findWhere(bodyParts, {headers: {'Content-Type': contentType}});
    }

    return function () {
      this.isSentMail = isSentMail;
      this.isDraftMail = isDraftMail;
      this.isInTrash = isInTrash;
      this.setDraftReplyFor = setDraftReplyFor;
      this.replyToAddress = replyToAddress;
      this.replyToAllAddress = replyToAllAddress;
      this.getMailMediaType = getMailMediaType;
      this.isMailMultipartAlternative = isMailMultipartAlternative;
      this.getMailMultiParts = getMailMultiParts;
      this.availableBodyPartsContentType = availableBodyPartsContentType;
      this.getMailPartByContentType = getMailPartByContentType;
      return this;
    };
  }());

  return {
    create: function (mail) {
      if (mail) {
        asMail.apply(mail);
      }
      return mail;
    }
  };
});
