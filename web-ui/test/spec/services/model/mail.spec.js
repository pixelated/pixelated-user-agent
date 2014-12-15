/*global Pixelated */

require(['services/model/mail'], function (Mail) {
  'use strict';

  describe('services/model/mail', function () {
    describe('parsing', function () {
      describe('a single email', function () {
        var sentMail, draftMail, receivedMail, receivedMailWithCC, rawMailWithMultipleTo;
        beforeEach(function () {
          sentMail = Mail.create(Pixelated.testData().rawMail.sent);
          draftMail = Mail.create(Pixelated.testData().rawMail.draft);
          receivedMail = Mail.create(Pixelated.testData().rawMail.received);
          receivedMailWithCC = Mail.create(Pixelated.testData().rawMail.receivedWithCC);
          rawMailWithMultipleTo = Mail.create(Pixelated.testData().rawMail.rawMailWithMultipleTo);
        });

        it('correctly identifies a sent mail', function () {
          expect(sentMail.isSentMail()).toBe(true);
        });

        it('correctly identifies a draft mail', function () {
          expect(draftMail.isDraftMail()).toBe(true);
        });

        it('correctly identifies a received mail', function () {
          expect(receivedMail.isSentMail()).toBe(false);
          expect(receivedMail.isDraftMail()).toBe(false);
        });
      });

      describe('multipart email', function () {
        var parsedMultipartMail;

        beforeEach(function () {
          parsedMultipartMail = Mail.create(Pixelated.testData().rawMail.multipart);
        });

        it('parses the mail as multipart/alternative', function () {
          expect(parsedMultipartMail.isMailMultipartAlternative()).toBe(true);
        });

        it('lists the correct available content-type of the parts', function () {
          expect(parsedMultipartMail.availableBodyPartsContentType()).toEqual(['text/plain;', 'text/html;']);
        });

        it('gets the list of parts', function () {
          var expectedParts = [
            {
              headers: { 'Content-Type': 'text/plain;' },
              body: 'Hello everyone!\n'
            },
            {
              headers: {
                'Content-Type': 'text/html;',
                'Content-Transfer-Encoding': 'quoted-printable'
              },
              body: '<p><b>Hello everyone!</b></p>\n'
            }
          ];

          expect(parsedMultipartMail.getMailMultiParts()).toEqual(expectedParts);
        });

        it('gets the text/plain body by the content-type', function () {
          expect(parsedMultipartMail.getMailPartByContentType('text/plain;')).toEqual(
            {
              headers: { 'Content-Type': 'text/plain;' },
              body: 'Hello everyone!\n'
            });
        });

        it('parses the content type of a text/html body', function () {
          expect(parsedMultipartMail.getMailPartByContentType('text/html;')).toEqual({
              headers: {
                'Content-Type': 'text/html;',
                'Content-Transfer-Encoding': 'quoted-printable'
              },
              body: '<p><b>Hello everyone!</b></p>\n'
          });
        });
      });
    });
  });
});
