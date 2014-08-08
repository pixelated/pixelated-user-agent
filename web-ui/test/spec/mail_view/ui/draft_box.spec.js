/* global Pixelated */

describeComponent('mail_view/ui/draft_box', function () {
  'use strict';

  var mail;

  beforeEach(function () {
    Pixelated.mockBloodhound();
    mail = Pixelated.testData().parsedMail.simpleTextPlain;
  });

  describe('when initializing', function () {
    it('fetches the email to draft', function () {
      var mailWantEvent = spyOnEvent(document, Pixelated.events.mail.want);

      setupComponent({mailIdent: '1'});

      expect(mailWantEvent).toHaveBeenTriggeredOnAndWith(document, {
        mail: '1', caller: this.component
      });
    });
  });

  describe('after initialize', function () {
    beforeEach(function () {
      setupComponent({mailIdent: '1'});
    });

    it('renders the compose box when mail is received', function () {
      var templates = require('views/templates');

      spyOn(this.component, 'render');

      this.component.trigger(this.component, Pixelated.events.mail.here, { mail: mail});

      expect(this.component.render).toHaveBeenCalledWith(templates.compose.box, {
        recipients: { to: mail.header.to, cc: mail.header.cc, bcc: mail.header.bcc },
        subject: mail.header.subject,
        body: mail.body
      });
    });

  });

  it('sending a draft sends the correct mailIdent', function () {
    setupComponent({mailIdent: mail.ident});
    this.component.trigger(this.component, Pixelated.events.mail.here, { mail: mail});

    var sendDraftEvent = spyOnEvent(document, Pixelated.events.mail.saveDraft);
    this.component.select('draftButton').click();

    expect(sendDraftEvent).toHaveBeenTriggeredOnAndWith(document, jasmine.objectContaining({ident: mail.ident}));
  });

  it('shows no message selected pane when draft is sent', function() {
    var openNoMessageSelectedEvent = spyOnEvent(document, Pixelated.events.dispatchers.rightPane.openNoMessageSelected);

    setupComponent({mailIdent: mail.ident});
    this.component.trigger(this.component, Pixelated.events.mail.here, { mail: mail});

    this.component.trigger(document, Pixelated.events.mail.sent);

    expect(openNoMessageSelectedEvent).toHaveBeenTriggeredOn(document);
  });

});
