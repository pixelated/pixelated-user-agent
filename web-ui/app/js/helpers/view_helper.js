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


  function formatFingerPrint(fingerprint) {
    fingerprint = fingerprint || '';
    return fingerprint.replace(/(.{4})/g, '$1 ').trim();
  }

  function getSinceDate(sinceDate){
    var commitDate = new Date(sinceDate);
    var number = Date.now();
    var millisecondsSince = number - commitDate;

    var SECONDS = 1000,
        MIN = 60 * SECONDS,
        HOUR = MIN * 60,
        DAY = HOUR * 24,
        WEEK = DAY * 7,
        MONTH = WEEK * 4,
        YEAR = DAY * 365;

    var years = Math.floor(millisecondsSince / YEAR);
    if (years >= 1){
      return years + ' year(s)';
    }

    var months = Math.floor(millisecondsSince / MONTH);
    if (months >= 1) {
      return months + ' month(s)';
    }

    var weeks = Math.floor(millisecondsSince / WEEK);
    if (weeks >= 1) {
      return weeks + ' week(s)';
    }

    var days = Math.floor(millisecondsSince / DAY);
    if (days >= 1) {
      return days + ' day(s)';
    }

    var hours = Math.floor(millisecondsSince / HOUR);
    if (hours >= 1) {
      return hours + ' hour(s)';
    }

    var minutes = Math.floor(millisecondsSince / MIN);
    return minutes + ' minute(s)';
  }

  Handlebars.registerHelper('formatDate', formatDate);
  Handlebars.registerHelper('formatSize', formatSize);
  Handlebars.registerHelper('formatStatusClasses', formatStatusClasses);
  Handlebars.registerHelper('formatFingerPrint', formatFingerPrint);
  Handlebars.registerHelper('sinceDate', getSinceDate);

  return {
    formatStatusClasses: formatStatusClasses,
    formatSize: formatSize,
    formatMailBody: formatMailBody,
    formatFingerPrint: formatFingerPrint,
    moveCaretToEndOfText: moveCaretToEndOfText,
    quoteMail: quoteMail,
    sinceDate: getSinceDate,
    i18n: i18n
  };
});
