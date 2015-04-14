describeComponent('mail_list/ui/mail_items/draft_item', function () {
  'use strict';

  var mail;

  beforeEach(function () {
    mail = Pixelated.testData().parsedMail.draft;

    this.setupComponent('<li></li>', {
      mail: mail,
      selected: false,
      templateType: 'single'
    });
  });

  it('should de-select the item if a new mail is composed', function () {
    this.component.$node.addClass('selected');

    $(document).trigger(Pixelated.events.ui.composeBox.newMessage);

    expect(this.component.$node).not.toHaveClass('selected');
  });

  it('should trigger the openDraft event when clicked', function () {
    var openDraftEvent = spyOnEvent(document, Pixelated.events.dispatchers.rightPane.openDraft);

    this.$node.find('a').click();

    expect(openDraftEvent).toHaveBeenTriggeredOnAndWith(document, { ident: 'B2432' });
  });
});

