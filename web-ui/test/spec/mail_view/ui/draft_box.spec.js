/* global Pixelated */

describeComponent('mail_view/ui/draft_box', function () {
  'use strict';

  var mail;

  beforeEach(function () {
    Pixelated.mockBloodhound();
    mail = Pixelated.testData().parsedMail.simpleTextPlain;
    spyOn($, 'getJSON').and.returnValue($.Deferred());
  });

  describe('when initializing', function () {
    it('fetches the email to draft', function () {
      var mailWantEvent = spyOnEvent(document, Pixelated.events.mail.want);

      this.setupComponent({mailIdent: '1'});

      expect(mailWantEvent).toHaveBeenTriggeredOnAndWith(document, {
        mail: '1', caller: this.component
      });
    });
  });

  describe('after initialize', function () {
    it('renders the compose box when mail is received', function () {
      this.setupComponent({mailIdent: '1'});
      var templates = require('views/templates');

      spyOn(this.component, 'render');

      this.component.trigger(this.component, Pixelated.events.mail.here, { mail: mail});

      expect(this.component.render).toHaveBeenCalledWith(templates.compose.box, {
        recipients: { to: mail.header.to, cc: mail.header.cc, bcc: mail.header.bcc },
        subject: mail.header.subject,
        body: mail.textPlainBody
      });
    });

  });

  it('shows no message selected pane when draft is sent', function() {
    var openNoMessageSelectedEvent = spyOnEvent(document, Pixelated.events.dispatchers.rightPane.openNoMessageSelected);

    this.setupComponent({mailIdent: mail.ident});
    this.component.trigger(this.component, Pixelated.events.mail.here, { mail: mail});

    this.component.trigger(document, Pixelated.events.mail.sent);

    expect(openNoMessageSelectedEvent).toHaveBeenTriggeredOn(document);
  });

  it('should call the enableFloatlabel method when events.mail.here is trigged', function() {
    this.setupComponent({mailIdent: mail.ident});
    spyOn(this.component, 'enableFloatlabel');

    this.component.trigger(this.component, Pixelated.events.mail.here, { mail: mail });

    expect(this.component.enableFloatlabel).toHaveBeenCalledWith('input.floatlabel');
    expect(this.component.enableFloatlabel).toHaveBeenCalledWith('textarea.floatlabel');
  });

});
