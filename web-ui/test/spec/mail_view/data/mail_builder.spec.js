define(['mail_view/data/mail_builder'], function (mailBuilder) {
  'use strict';
  describe('mail builder', function () {

    it('sets ident if passed to constructor', function() {
      var mail = mailBuilder.newMail('12345').build();

      expect(mail.ident).toBe('12345');
    });

    it('sets ident to empty if not passed to constructor', function() {
      var mail = mailBuilder.newMail().build();

      expect(mail.ident).toBe('');
    });

    it('sets the subject', function() {
      var mail = mailBuilder.newMail().subject('subject').build();

      expect(mail.header.subject).toBe('subject');
    });

    it('sets the body', function() {
      var mail = mailBuilder.newMail().body('some body text').build();

      expect(mail.body).toBe('some body text');
    });

    describe('to field', function() {
      it('adds a single address', function() {
        var mail = mailBuilder.newMail().to('foo@bar.com').build();

        expect(mail.header.to).toContain('foo@bar.com');
      });

      it('adds multiple addresses', function() {
        var mail = mailBuilder.newMail().to('foo@bar.com bar@foo.com').build();

        expect(mail.header.to).toContain('foo@bar.com');
        expect(mail.header.to).toContain('bar@foo.com');
      });

      it('accepts undefined without breaking', function() {
        var mail = mailBuilder.newMail().to(undefined).build();

        expect(mail.header.to).toEqual([]);
      });
    });

    describe('cc field', function() {
      it('adds a single address', function() {
        var mail = mailBuilder.newMail().cc('foo@bar.com').build();

        expect(mail.header.cc).toContain('foo@bar.com');
      });

      it('adds multiple addresses', function() {
        var mail = mailBuilder.newMail().cc('foo@bar.com bar@foo.com').build();

        expect(mail.header.cc).toContain('foo@bar.com');
        expect(mail.header.cc).toContain('bar@foo.com');
      });

      it('accepts undefined without breaking', function() {
        var mail = mailBuilder.newMail().cc(undefined).build();

        expect(mail.header.cc).toEqual([]);
      });
    });

    describe('bcc field', function() {
      it('adds a single address', function() {
        var mail = mailBuilder.newMail().bcc('foo@bar.com').build();

        expect(mail.header.bcc).toContain('foo@bar.com');
      });

      it('adds multiple addresses', function() {
        var mail = mailBuilder.newMail().bcc('foo@bar.com bar@foo.com').build();

        expect(mail.header.bcc).toContain('foo@bar.com');
        expect(mail.header.bcc).toContain('bar@foo.com');
      });

      it('accepts undefined without breaking', function() {
        var mail = mailBuilder.newMail().bcc(undefined).build();

        expect(mail.header.bcc).toEqual([]);
      });
    });

    it('adds arbitrary headers', function() {
      var mail = mailBuilder.newMail()
        .header('Reply-To', 'something')
        .header('In-Reply-To', '12345')
        .build();

      expect(mail.header['Reply-To']).toBe('something');
      expect(mail.header['In-Reply-To']).toBe('12345');
    });

    it('adds tag', function() {
      var mail = mailBuilder.newMail()
        .tag('tag1')
        .build();

      expect(mail.tags).toContain('tag1');
    });
  });
});
