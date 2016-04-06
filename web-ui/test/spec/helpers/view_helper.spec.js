define(['helpers/view_helper'], function (viewHelper) {
  'use strict';

  var testData;
  describe('view helper', function() {
    beforeEach(function () {
      testData = Pixelated.testData();
    });

    describe('quote email', function() {
      it('should add > to body text', function() {
        testData.parsedMail.simpleTextPlain.textPlainBody = 'First Line\nSecond Line';

        var quotedMail = viewHelper.quoteMail(testData.parsedMail.simpleTextPlain);

        expect(quotedMail).toContain('> First Line\n> Second Line');
      });

      it('should add the mail sender information', function() {
        testData.parsedMail.simpleTextPlain.textPlainBody = 'First Line\nSecond Line';

        var quotedMail = viewHelper.quoteMail(testData.parsedMail.simpleTextPlain);

        expect(quotedMail).toContain('<laurel@hamill.info>');
      });
    });

    describe('formatDate', function() {
      var template;
      beforeEach(function () {
        template = Handlebars.compile('{{formatDate date}}');
      });

      it('formats correctly a Date for today', function() {
        var d = new Date();
        var mailDate = new Date(d.getFullYear(), d.getMonth(), d.getDate(), 14, 2, 36);

        var result = template({ date: mailDate.toISOString() });

        expect(result).toEqual('14:02');
      });

      it('formats correctly a Date for a specific day', function() {
        var mailDate = new Date(2013, 2, 13, 7, 56, 1);

        var result = template({ date: mailDate.toISOString() });

        // This expectation is weird for the month - JS Dates have date numbers be zero-indexed, thus the discrepancy
        // Specifically, the 2 in the constructor DOES match the 3 in the expectation below.
        expect(result).toEqual('2013-03-13');
      });
    });

    describe('formatSize', function() {
      var template;
      beforeEach(function () {
        template = Handlebars.compile('{{formatSize size}}');
      });

      it('formats size to bytes', function() {
        var bytes = 42;
        var result = template({ size: bytes });
        expect(result).toEqual('42.00  b');
      });

      it('formats size to kilobytes', function() {
        var bytes = 4200;
        var result = template({ size: bytes });
        expect(result).toEqual('4.10 Kb');
      });

      it('formats size to megabytes', function() {
        var bytes = 4200000;
        var result = template({ size: bytes });
        expect(result).toEqual('4.01 Mb');
      });
    });

    describe('format status classes', function () {
      it('formats all the status of the email to css classes', function () {
        var statuses = ['read', 'banana'];

        expect(viewHelper.formatStatusClasses(statuses)).toEqual('status-read status-banana');
      });

      it('formats a single status of the email to a css class', function () {
        var statuses = ['read'];

        expect(viewHelper.formatStatusClasses(statuses)).toEqual('status-read');
      });
    });

    it('escape html in plain text body', function () {
      var formattedMail = $('<div></div>');
      var mail = testData.parsedMail.simpleTextPlain;
      mail.textPlainBody = '<font color="red">This is some text!</font>';
      formattedMail.html(viewHelper.formatMailBody(mail));
      expect(formattedMail.text()).toBe('<font color="red">This is some text!</font>');

    });

    it('move caret to the end of text after 1ms', function () {
      spyOn(window, 'setTimeout');

      viewHelper.moveCaretToEndOfText();

      expect(window.setTimeout.calls.all()[0].args[1]).toEqual(1);
    });

    describe('fingerprint helper', function () {
      it('should format fingerprint', function () {
        expect(viewHelper.formatFingerPrint('12345678')).toEqual('1234 5678');
      });
    });
  });
});
