describeComponent('mail_view/ui/reply_section', function () {
  'use strict';

  beforeEach(function () {
    this.setupComponent();
  });

  describe('show/hide reply container', function () {
    it('should hide reply container until mail data is loaded', function () {
      this.component.checkForDraftReply();
      expect(this.component.select('replyContainer')).toBeHidden();
    });

    it('should show reply container when mail data is loaded', function () {
      this.component.trigger(document, Pixelated.events.ui.replyBox.showReplyContainer);
      expect(this.component.select('replyContainer')).not.toBeHidden();
    });
  });

  describe('clicking reply buttons', function() {
    var mailWantEvent, expectEventData;

    beforeEach(function () {
      mailWantEvent = spyOnEvent(document, Pixelated.events.mail.want);
      expectEventData = {
        mail: '12345',
        caller: this.component
      };
      this.component.attr.ident = '12345';
    });

    it('should ask for email when clicking on reply button', function() {
      this.component.select('replyButton').click();

      expect(mailWantEvent).toHaveBeenTriggeredOnAndWith(document, expectEventData);
    });

    it('should ask for email when clicking on replyAll button', function() {
      this.component.select('replyAllButton').click();

      expect(mailWantEvent).toHaveBeenTriggeredOnAndWith(document, expectEventData);
    });
  });

  describe('creating reply box when getting email back', function() {
    var mailData, ReplyBox, ForwardBox;

    beforeEach(function () {
      mailData = Pixelated.testData().mail;
      ReplyBox = require('mail_view/ui/reply_box');
      ForwardBox = require('mail_view/ui/forward_box');
      spyOn(ReplyBox, 'attachTo');
      spyOn(ForwardBox, 'attachTo');
    });

    it('for normal reply', function() {
      this.component.attr.replyType = 'reply';
      this.component.trigger(this.component, Pixelated.events.mail.here, { mail: mailData });

      expect(this.component.select('replyContainer')).not.toBeHidden();
      expect(ReplyBox.attachTo).toHaveBeenCalledWith(jasmine.any(Object), {
        mail: mailData,
        replyType: 'reply'
      });
    });

    it('for reply to all', function() {
      this.component.attr.replyType = 'replyall';
      this.component.trigger(this.component, Pixelated.events.mail.here, { mail: mailData });

      expect(this.component.select('replyContainer')).not.toBeHidden();
      expect(ReplyBox.attachTo).toHaveBeenCalledWith(jasmine.any(Object), {
        mail: mailData,
        replyType: 'replyall'
      });
    });

    it('creates a forward box', function() {
      this.component.attr.replyType = 'forward';
      this.component.trigger(this.component, Pixelated.events.mail.here, { mail: mailData });

      expect(this.component.select('replyContainer')).not.toBeHidden();
      expect(ForwardBox.attachTo).toHaveBeenCalledWith(jasmine.any(Object), {
        mail: mailData
      });
    });
  });

  it('hides the buttons when clicked', function() {
    this.component.attr.mailIdent = 12345;

    this.component.select('replyButton').click();

    expect(this.component.select('replyButton')).toBeHidden();
    expect(this.component.select('replyAllButton')).toBeHidden();
    expect(this.component.select('forwardButton')).toBeHidden();
  });

  it('shows the buttons when reply is cancelled', function() {
    this.component.attr.mailIdent = 12345;
    this.component.select('replyButton').click();

    $(document).trigger(Pixelated.events.ui.composeBox.trashReply);

    expect(this.component.select('replyContainer')).not.toBeHidden();
    expect(this.component.select('replyButton')).not.toBeHidden();
    expect(this.component.select('replyAllButton')).not.toBeHidden();
    expect(this.component.select('forwardButton')).not.toBeHidden();
  });
});
