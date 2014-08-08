describeComponent('mail_list/ui/mail_items/generic_mail_item', function () {
  'use strict';

  var mail;

  beforeEach(function () {
    mail = Pixelated.testData().parsedMail.simpleTextPlain;
    mail.tags = ['inbox'];

    setupComponent('<li></li>', {
      mail: mail,
      selected: false,
      tag: 'inbox'
    });
  });

  it('should trigger ui:openMail on click', function () {
    var spyEvent = spyOnEvent(document, Pixelated.events.ui.mail.open);

    this.component.$node.find('a').click();

    expect(spyEvent).toHaveBeenTriggeredOn(document);
    expect(spyEvent.mostRecentCall.data).toEqual({ ident: mail.ident });
  });

  it('should add selected class when selecting', function () {
    this.$node.find('a').click();

    expect(this.$node).toHaveClass('selected');
  });

  it('should remove selected class when selecting a different mail', function () {
    $(document).trigger(Pixelated.events.ui.mail.updateSelected, { ident: 2 });

    expect(this.$node).not.toHaveClass('selected');
  });

  it('should remove selected class when enabling compose box', function () {
    this.$node.find('a').click();

    $(document).trigger(Pixelated.events.ui.composeBox.newMessage);

    expect(this.$node).not.toHaveClass('selected');
  });

  it('should have the href link with mail ident and tag name', function () {
    expect(this.$node.find('a')[0].href).toMatch('inbox/mail/' + mail.ident);
  });

  describe('clicking on a mail', function () {

    function createClickEvent(options) {
      var clickEvent = $.Event('click');
      _.merge(clickEvent, options);
      spyOn(clickEvent, 'preventDefault');
      return clickEvent;
    }

    it('triggers mail open and pushes the state', function () {
      var clickEvent = createClickEvent();
      var mailOpenEvent = spyOnEvent(document, Pixelated.events.ui.mail.open);
      var pushStateEvent = spyOnEvent(document, Pixelated.events.router.pushState);

      $(this.$node.find('a')).trigger(clickEvent);

      expect(mailOpenEvent).toHaveBeenTriggeredOnAndWith(document, { ident: mail.ident });
      expect(pushStateEvent).toHaveBeenTriggeredOnAndWith(document, { mailIdent: mail.ident });
      expect(clickEvent.preventDefault).toHaveBeenCalled();
    });

    describe('when opening on a new tab', function () {

      _.each([
        {metaKey: true},
        {which: 2},
        {ctrlKey: true}
      ], function (specialKey) {
        it('doesnt trigger mail open and nor pushes the state', function () {
          var clickEvent = createClickEvent(specialKey);
          var mailOpenEvent = spyOnEvent(document, Pixelated.events.ui.mail.open);
          var pushStateEvent = spyOnEvent(document, Pixelated.events.router.pushState);

          $(this.$node.find('a')).trigger(clickEvent);

          expect(mailOpenEvent).not.toHaveBeenTriggeredOnAndWith(document, { ident: mail.ident });
          expect(pushStateEvent).not.toHaveBeenTriggeredOnAndWith(document, { mailIdent: mail.ident });
          expect(clickEvent.preventDefault).not.toHaveBeenCalled();
        });

        it('marks the email as read', function () {
          debugger;
          var mailReadEvent = spyOnEvent(document, Pixelated.events.mail.read);
          var clickEvent = createClickEvent(specialKey);

          $(this.$node.find('a')).trigger(clickEvent);

          expect(this.component.attr.mail.status).toContain(this.component.status.READ);
          expect(this.$node.attr('class')).toMatch('status-read');
          expect(mailReadEvent).toHaveBeenTriggeredOnAndWith(document, { ident: mail.ident, tags: ['inbox'] });
        });

      });

    });

  });

  describe('marking emails as read', function () {
    it('should trigger mail:read event when unread is clicked', function () {
      var mailReadEvent = spyOnEvent(document, Pixelated.events.mail.read);

      this.$node.find('a').click();

      expect(mailReadEvent).toHaveBeenTriggeredOnAndWith(document, jasmine.objectContaining({ident: mail.ident}));
    });

    it('should not trigger mail:read event when clicking mail that is already read', function () {
      var mailReadEvent = spyOnEvent(document, Pixelated.events.mail.read);
      this.component.attr.mail.status.push(this.component.status.READ);

      this.$node.find('a').click();

      expect(mailReadEvent).not.toHaveBeenTriggeredOnAndWith(document, {ident: mail.ident});
    });

    it('should add status-read class to email when clicking an unread email', function () {
      this.$node.find('a').click();

      expect(this.$node).toHaveClass('status-read');
    });

    it('should not have status-read class when initializing email without read status', function () {
      expect(this.$node).not.toHaveClass('status-read');
    });
  });
});
