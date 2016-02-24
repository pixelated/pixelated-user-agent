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
    'views/i18n',
    'quoted-printable/quoted-printable',
    'utf8/utf8',
    'helpers/sanitizer'
  ],
  function(contentType, i18n, quotedPrintable, utf8, sanitizer) {
  'use strict';

  function formatStatusClasses(ss) {
    return _.map(ss, function(s) {
      return 'status-' + s;
    }).join(' ');
  }

  function formatMailBody(mail) {
    return sanitizer.sanitize(mail);
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

  function prependFrom(mail) {
    return i18n(
      'On __date__, <__from__> wrote:\n',
      {'date': new Date(mail.header.date).toString(), 'from': mail.header.from}
    );
  }

  function quoteMail(mail) {
    return '\n\n' + prependFrom(mail) + mail.textPlainBody.replace(/^/mg, '> ');
  }

  function formatDate(dateString) {
    var date = new Date(dateString);
    var today = createTodayDate();
    if (date.getTime() > today.getTime()) {
      return fixedSizeNumber(date.getHours(), 2) + ':' + fixedSizeNumber(date.getMinutes(), 2);
    } else {
      return '' + date.getFullYear() + '-' + fixedSizeNumber(date.getMonth() + 1, 2) + '-' + fixedSizeNumber(date.getDate(), 2);
    }
  }

  function formatSize(bytes) {
    var e = Math.floor(Math.log(bytes) / Math.log(1024));
    return (bytes / Math.pow(1024, e)).toFixed(2) + ' ' + ' KMGTP'.charAt(e) + 'b';
  }


  Handlebars.registerHelper('formatDate', formatDate);
  Handlebars.registerHelper('formatSize', formatSize);
  Handlebars.registerHelper('formatStatusClasses', formatStatusClasses);

  return {
    formatStatusClasses: formatStatusClasses,
    formatSize: formatSize,
    formatMailBody: formatMailBody,
    moveCaretToEndOfText: moveCaretToEndOfText,
    quoteMail: quoteMail,
    i18n: i18n
  };
});
