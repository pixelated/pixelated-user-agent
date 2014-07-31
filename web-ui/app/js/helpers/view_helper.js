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
    return bodyPart.headers['Content-Transfer-Encoding'] && bodyPart.headers['Content-Transfer-Encoding'] === 'quoted-printable';
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
    } else {
      body = bodyPart.body;
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

      return $(addParagraphsToPlainText(mail.getMailMultiParts[0]));
    }

    return $(addParagraphsToPlainText(mail.body));

    /*
    var body;
    // probably parse MIME parts and ugliness here
    // content_type: "multipart/alternative;  boundary="----=_Part_1115_17865397.1370312509342""
    var mediaType = new contentType.MediaType(mail.header.content_type);
    if(mediaType.type === 'multipart/alternative') {
      var parsedBodyParts = getMailMultiParts(mail.body, mediaType);
      var selectedBodyPart = getHtmlMailPart(parsedBodyParts) || getPlainTextMailPart(parsedBodyParts) || parsedBodyParts[0];
      body = selectedBodyPart.body;

      if (isQuotedPrintableBodyPart(selectedBodyPart)) {
        body = quotedPrintable.decode(body);
      }
    } else {
      body = addParagraphsToPlainText(mail.body);
    }
    return $(htmlWhitelister.sanitize(body, htmlWhitelister.tagPolicy));
    */
  }

  function moveCaretToEnd(el) {
    if (typeof el.selectionStart == "number") {
      el.selectionStart = el.selectionEnd = el.value.length;
    } else if (typeof el.createTextRange != "undefined") {
      el.focus();
      var range = el.createTextRange();
      range.collapse(false);
      range.select();
    }
  }

  function fixedSizeNumber(num, size) {
    var res = num.toString();
    while(res.length < size) {
      res = "0" + res;
    }
    return res;
  }

  function getFormattedDate(date){
    var today = createTodayDate();
    if (date.getTime() > today.getTime()) {
      return fixedSizeNumber(date.getHours(), 2) + ":" + fixedSizeNumber(date.getMinutes(), 2);
    } else {
      return "" + date.getFullYear() + "-" + fixedSizeNumber(date.getMonth() + 1, 2) + "-" + fixedSizeNumber(date.getDate(), 2);
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
