define([], function() {
  'use strict';
  function toBeRenderedInMatcher () {
    return {
      compare: function (mail, node) {
        var result = {}, equals = {}, subject, tags, from, date, messages = [], notMessages = [];

        subject = node.find('#mail-' + mail.ident + ' .subject-and-tags')[0];
        tags = _.map(node.find('#mail-' + mail.ident + ' .subject-and-tags .tag'), function (tag) { return tag.textContent; });
        date = node.find('#mail-' + mail.ident + ' .received-date');
        from = node.find('#mail-' + mail.ident + ' .from');

        if (subject && subject.textContent.trim() === mail.header.subject) {
          equals.subject = true;
          notMessages.push('not to be rendered with subject ' + mail.header.subject);
        } else {
          equals.subject = false;
          messages.push('to be rendered with subject ' + mail.header.subject + ', but was rendered with subject ' + subject.textContent.trim());
        }

        if (tags && tags.join(', ') === mail.tags.join(', ')) {
          equals.tags = true;
          notMessages.push('not to be rendered with tags ' + mail.tags.join(', '));
        } else {
          equals.tags = false;
          messages.push('to be rendered with tags ' + mail.tags.join(', ') + ', but was rendered with tags ' + tags.join(', '));
        }

        if (date && date.text().trim() === mail.header.date.split('T')[0]) {
          equals.date = true;
          notMessages.push('not to be rendered with date ' + mail.header.date.split('T')[0]);
        } else {
          equals.date = false;
          messages.push('to be rendered with date ' + mail.header.date.split('T')[0] + ', but was rendered with date ' + date.text().trim());
        }

        if (from && from.text().trim() === mail.header.from) {
          equals.from = true;
          notMessages.push('not to be rendered with from ' + mail.header.from);
        } else {
          equals.from = false;
          messages.push('to be rendered with from ' + mail.header.from + ', but was rendered with from ' + from.text().trim());
        }

        result.pass = equals.subject && equals.tags && equals.date && equals.from;

        if (result.pass) {
          result.message = 'Expected mail ' + mail.ident + ' ' + notMessages.join(', ');
        } else {
          result.message = 'Expected mail ' + mail.ident + ' ' + messages.join(', ');
        }

        return result;
      }
    };
  }

  function toBeRenderedSelectedInMatcher () {
    return {
      compare: function (mail, node) {
        var result = {}, toBeRendered, mailNode;

        toBeRendered = toBeRenderedInMatcher().compare(mail, node);

        mailNode = node.find('#mail-' + mail.ident);
        result.pass = toBeRendered.pass && mailNode.hasClass('selected');

        if (result.pass) {
          result.message = toBeRendered.message + '\nExpected mail ' + mail.ident + ' to not be selected in ' + mailNode.html();
        } else {
          result.message = toBeRendered.message + '\nExpected mail ' + mail.ident + ' to be selected in ' + mailNode.html();
        }

        return result;
      }
    };
  }

  return {
    toBeRenderedIn: toBeRenderedInMatcher,
    toBeRenderedSelectedIn: toBeRenderedSelectedInMatcher
  };
});

