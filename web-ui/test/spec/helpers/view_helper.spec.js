define(['helpers/view_helper'], function (viewHelper) {
  'use strict';

  var testData;
  describe('view helper', function() {
    beforeEach(function () {
      testData = Pixelated.testData();
    });

    describe('quote email', function() {
      it('should add > to body text', function() {
        testData.rawMail.mail.textPlainBody = 'First Line\nSecond Line';

        var quotedMail = viewHelper.quoteMail(testData.rawMail.mail);

        expect(quotedMail).toContain('> First Line\n> Second Line');
      });
    });

    describe('getFormmattedDate', function() {
      it('formats correctly a Date for today', function() {
        var d = new Date();
        var dtest = new Date(d.getFullYear(), d.getMonth(), d.getDate(), 14, 2, 36);

        var res = viewHelper.getFormattedDate(dtest);

        expect(res).toEqual('14:02');

      });

      it('formats correctly a Date for a specific day', function() {
        var dtest = new Date(2013, 2, 13, 7, 56, 1);

        var res = viewHelper.getFormattedDate(dtest);

        // This expectation is weird for the month - JS Dates have date numbers be zero-indexed, thus the discrepancy
        // Specifically, the 2 in the constructor DOES match the 3 in the expectation below.
        expect(res).toEqual('2013-03-13');
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

    it('each line of plain text mail gets a new paragraph', function () {
      var formattedMail = $('<div></div>');
      formattedMail.html(viewHelper.formatMailBody(testData.parsedMail.simpleTextPlain));
      expect(formattedMail).toContainHtml('<div>Hello Everyone<br/></div>');
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
  });
});
