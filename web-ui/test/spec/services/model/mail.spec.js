/*global Pixelated */

require(['services/model/mail'], function (Mail) {
  'use strict';
  var testData;

  describe('services/model/mail', function () {
    describe('reply addresses', function () {
      it('returns the "to" and "cc" addresses if the mail was sent', function () {
        var mail = Mail.create({
          header: { to: ['a@b.c', 'e@f.g'], cc: ['x@x.x'] },
          tags: ['sent']
        });

        var addresses = mail.replyToAddress();

        expect(addresses).toEqual({ to: ['a@b.c', 'e@f.g'], cc: ['x@x.x']});
      });
    });

    describe('parsing', function () {
      describe('a single email', function () {
        var sentMail, draftMail, recievedMail, recievedMailWithCC;
        beforeEach(function () {
          sentMail = Mail.create(Pixelated.testData().rawMail.sent);
          draftMail = Mail.create(Pixelated.testData().rawMail.draft);
          recievedMail = Mail.create(Pixelated.testData().rawMail.recieved);
          recievedMailWithCC = Mail.create(Pixelated.testData().rawMail.recievedWithCC);
        });

        it('correctly identifies a sent mail', function () {
          expect(sentMail.isSentMail()).toBe(true);
        });

        it('correctly identifies a draft mail', function () {
          expect(draftMail.isDraftMail()).toBe(true);
        });

        it('correctly identifies a recieved mail', function () {
          expect(recievedMail.isSentMail()).toBe(false);
          expect(recievedMail.isDraftMail()).toBe(false);
        });

        it('reply to of a sent mail should be original recipient', function () {
          expect(sentMail.replyToAddress()).toEqual({to: ['mariane_dach@davis.info'], cc: ['duda@la.lu']});
        });

        it('reply to of a mail should be the reply_to field if existent', function () {
          expect(recievedMail.replyToAddress()).toEqual({to: ['afton_braun@botsford.biz'], cc: [] });
        });

        it('reply to of a mail should be the from field if no reply_to present', function () {
          expect(recievedMailWithCC.replyToAddress()).toEqual({to: ['cleve_jaskolski@schimmelhirthe.net'], cc: []});
        });

        it('reply to all should include all email addresses in the header', function () {
          expect(recievedMailWithCC.replyToAllAddress()).toEqual({
            to: ['cleve_jaskolski@schimmelhirthe.net', 'stanford@sipes.com'],
            cc: ['mariane_dach@davis.info']
          });
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
