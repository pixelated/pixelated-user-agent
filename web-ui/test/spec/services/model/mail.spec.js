require(['services/model/mail'], function (Mail) {
  'use strict';

  describe('services/model/mail', function () {
    describe('parsing', function () {
      describe('a single email', function () {
        var sentMail, draftMail, receivedMail, receivedMailWithCC, rawMailWithMultipleTo, mailInTrash;
        beforeEach(function () {
          sentMail = Mail.create(Pixelated.testData().rawMail.sent);
          draftMail = Mail.create(Pixelated.testData().rawMail.draft);
          mailInTrash = Mail.create(Pixelated.testData().rawMail.trash);
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

        it('correctly identifies a mail in trash', function () {
          expect(mailInTrash.isInTrash()).toBe(true);
        });
      });

    });
  });
});
