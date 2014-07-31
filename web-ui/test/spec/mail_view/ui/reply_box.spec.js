/*global jasmine */
/*global Smail */

describeComponent('mail_view/ui/reply_box', function () {
  'use strict';

  var attrs, i18n;
  beforeEach(function () {
    attrs = {
      mail: Smail.testData().parsedMail.simpleTextPlain
    };
    setupComponent(attrs);
    i18n = require('views/i18n');
  });

  describe('reply compose box', function() {
    it('should display subject of the reply', function() {
      expect(this.component.select('subjectDisplay').text()).toBe(i18n('Re: ') + attrs.mail.header.subject);
    });

    it('should show recipient fields when clicking on recipient display', function() {
      this.component.select('recipientsDisplay').click();

      expect(this.component.select('recipientsFields')).not.toBeHidden();
      expect(this.component.select('recipientsDisplay')).toBeHidden();
    });

    it('should show subject field when clicking on subject display', function() {
      this.component.select('subjectDisplay').click();

      expect(this.component.select('subjectInput')).not.toBeHidden();
      expect(this.component.select('subjectDisplay')).toBeHidden();
    });

    it('should use the from field when Reply-To header does not exist', function() {
      attrs.mail.header.reply_to = undefined;

      setupComponent(attrs);

      expect(this.component.attr.recipientValues['to']).toEqual([attrs.mail.header.from]);
    });

    it('should have a subject of Re: <original_message>', function() {
      attrs.mail.header.subject = 'Very interesting';

      setupComponent(attrs);

      expect(this.component.select('subjectDisplay').text()).toEqual(i18n('Re: ')+ attrs.mail.header.subject);
    });

    it('should use set In-Reply-To header when Message-Id header is set', function() {
      var mailSendEvent = spyOnEvent(document, Smail.events.mail.send);

      attrs.mail.header.message_id = '12345';
      setupComponent(attrs);

      $(document).trigger(Smail.events.ui.mail.send);

      expect(mailSendEvent).toHaveBeenTriggeredOn(document);
      expect(mailSendEvent.mostRecentCall.data.header).toEqual(jasmine.objectContaining({
        in_reply_to: '12345'
      }));
    });

    it('keeps the List-Id header when it exists', function() {
      var mailSendEvent = spyOnEvent(document, Smail.events.mail.send);
      attrs.mail.header.list_id = 'somelist';

      setupComponent(attrs);
      $(document).trigger(Smail.events.ui.mail.send);

      expect(mailSendEvent.mostRecentCall.data.header).toEqual(jasmine.objectContaining({
        list_id: 'somelist'
      }));
    });

    it('populates body text area with quote of email being replied', function() {
      var viewHelper = require('helpers/view_helper');
      spyOn(viewHelper, 'quoteMail').andReturn('quoted email');

      setupComponent(attrs);

      expect(viewHelper.quoteMail).toHaveBeenCalledWith(attrs.mail);
      expect(this.component.select('bodyBox').val()).toBe('quoted email');
    });

    it('triggers mail when cancelling a reply', function () {
      var mailSaveEvent = spyOnEvent(document, Smail.events.mail.save);

      this.component.select('trashButton').click();

      expect(mailSaveEvent).toHaveBeenTriggeredOn(document);
    });

    it('reopens the mail after the reply is sent', function () {
      var mailOpenEvent = spyOnEvent(document, Smail.events.ui.mail.open);

      this.component.trigger(document, Smail.events.mail.sent);

      expect(mailOpenEvent).toHaveBeenTriggeredOnAndWith(document, {
        ident: this.component.attr.mail.ident
      });
    });
  });
});
