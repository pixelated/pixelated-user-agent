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
define(
  [
    'helpers/contenttype',
    'lib/html_whitelister',
    'views/i18n',
    'quoted-printable/quoted-printable'
  ],
  function(contentType, htmlWhitelister, i18n_lib, quotedPrintable) {
  'use strict';

  function formatStatusClasses(ss) {
    return _.map(ss, function(s) {
      return 'status-' + s;
    }).join(' ');
  }

  function addParagraphsToPlainText(plainTextBodyPart) {
    return _.map(plainTextBodyPart.split('\n'), function (paragraph) {
      return '<p>' + paragraph + '</p>';
    }).join('');
  }

  function isQuotedPrintableBodyPart (bodyPart) {
    return bodyPart.headers &&
      bodyPart.headers['Content-Transfer-Encoding'] &&
      bodyPart.headers['Content-Transfer-Encoding'] === 'quoted-printable';
  }

  function getHtmlContentType (mail) {
    return _.find(mail.availableBodyPartsContentType(), function (contentType) {
      return contentType.indexOf('text/html') >= 0;
    });
  }

  function getSanitizedAndDecodedMailBody (bodyPart) {
    var body;

    if (isQuotedPrintableBodyPart(bodyPart)) {
      body = quotedPrintable.decode(bodyPart.body);
    } else if (bodyPart.body) {
      body = bodyPart.body;
    } else {
      body = bodyPart;
    }

    return htmlWhitelister.sanitize(body, htmlWhitelister.tagPolicy);
  }

  function formatMailBody (mail) {
    if (mail.isMailMultipartAlternative()) {
      var htmlContentType;

      htmlContentType = getHtmlContentType(mail);

      if (htmlContentType) {
        return $(getSanitizedAndDecodedMailBody(mail.getMailPartByContentType(htmlContentType)));
      }

      return $(getSanitizedAndDecodedMailBody(addParagraphsToPlainText(mail.getMailMultiParts[0])));
    }

    return $(getSanitizedAndDecodedMailBody(addParagraphsToPlainText(mail.body)));
  }

  function moveCaretToEnd(el) {
    if (typeof el.selectionStart === 'number') {
      el.selectionStart = el.selectionEnd = el.value.length;
    } else if (typeof el.createTextRange !== 'undefined') {
      el.focus();
      var range = el.createTextRange();
      range.collapse(false);
      range.select();
    }
  }

  function fixedSizeNumber(num, size) {
    var res = num.toString();
    while(res.length < size) {
      res = '0' + res;
    }
    return res;
  }

  function getFormattedDate(date){
    var today = createTodayDate();
    if (date.getTime() > today.getTime()) {
      return fixedSizeNumber(date.getHours(), 2) + ':' + fixedSizeNumber(date.getMinutes(), 2);
    } else {
      return '' + date.getFullYear() + '-' + fixedSizeNumber(date.getMonth() + 1, 2) + '-' + fixedSizeNumber(date.getDate(), 2);
    }
  }

  function createTodayDate() {
    var today = new Date();
    today.setHours(0);
    today.setMinutes(0);
    today.setSeconds(0);
    return today;
  }

  function moveCaretToEndOfText() {
    var self = this;

    moveCaretToEnd(self);
    window.setTimeout(function() {
      moveCaretToEnd(self);
    }, 1);
  }

  function quoteMail(mail) {
    var quotedLines = _.map(mail.body.split('\n'), function (line) {
      return '> ' + line;
    });

    return '\n\n' + quotedLines.join('\n');
  }

  function i18n(text) {
    return i18n_lib.get(text);
  }

  return {
    formatStatusClasses: formatStatusClasses,
    formatMailBody: formatMailBody,
    moveCaretToEndOfText: moveCaretToEndOfText,
    getFormattedDate: getFormattedDate,
    quoteMail: quoteMail,
    i18n: i18n
  };
});
