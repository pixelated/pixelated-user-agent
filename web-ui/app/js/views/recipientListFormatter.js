/*global Handlebars */

define(function() {
  'use strict';
  Handlebars.registerHelper('formatRecipients', function (header) {
    function wrapWith(begin, end) {
      return function (x) { return begin + x + end; };
    }

    var to = _.map(header.to, wrapWith('<span class="to">', '</span>'));
    var cc = _.map(header.cc, wrapWith('<span class="cc">cc: ', '</span>'));
    var bcc = _.map(header.bcc, wrapWith('<span class="bcc">bcc: ', '</span>'));

    return new Handlebars.SafeString(to.concat(cc, bcc).join(', '));
  });
});
