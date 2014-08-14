/*global _ */
'use strict';

define(['helpers/contenttype'],
  function (contentType) {

  var asMail = (function () {

    function isSentMail() {
      return _.contains(this.tags, 'sent');
    }

    function isDraftMail() {
      return _.contains(this.tags, 'drafts');
    }

    function normalize(recipients) {
      return _.chain([recipients])
        .flatten()
        .filter(function (r) {
          return !_.isUndefined(r) && !_.isEmpty(r);
        })
        .value();
    }

    function isInTrash() {
      return _.contains(this.tags, 'trash');
    }

    function setDraftReplyFor(ident) {
      this.draft_reply_for = ident;
    }

    function recipients(){
      return {
        to: normalize(this.header.to),
        cc: normalize(this.header.cc)
      };
    }

    function replyToAddress() {
      var recipients;

      if (this.isSentMail()) {
        recipients = this.recipients();
      } else {
        recipients = {
          to: normalize(this.header.reply_to || this.header.from),
          cc: []
        };
      }

      return recipients;
    }

    function replyToAllAddress() {
      return {
        to: normalize([this.header.reply_to, this.header.from, this.header.to]),
        cc: normalize(this.header.cc)
      };
    }

    function getHeadersFromMailPart (rawBody) {
      var lines, headerLines, endOfHeaders, headers;

      lines = rawBody.split('\n');
      endOfHeaders = _.indexOf(lines, '');
      headerLines = lines.slice(0, endOfHeaders);

      headers = _.map(headerLines, function (headerLine) {
        return headerLine.split(': ');
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
    };

    function getMailMediaType () {
      return new contentType.MediaType(this.header['Content-Type']);
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
      this.recipients = recipients;
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
