describeMixin('mail_list/ui/mail_items/mail_item', function () {
  'use strict';

  beforeEach(function () {
    var mail = Pixelated.testData().parsedMail.simpleTextPlain;
    mail.tags = ['inbox'];

    this.setupComponent('<li><input type="checkbox"></input></li>', {
      mail: mail,
      selected: false,
      tag: 'inbox'
    });
  });

  describe('mail checkbox', function () {
    var mailCheckedEvent, mailUncheckedEvent, checkbox;
    beforeEach(function () {
      mailCheckedEvent = spyOnEvent(document, Pixelated.events.ui.mail.checked);
      mailUncheckedEvent = spyOnEvent(document, Pixelated.events.ui.mail.unchecked);
      checkbox = this.component.$node.find('input[type=checkbox]');
    });

    it('unchecks itself when another tag is selected', function () {
      this.component.checkCheckbox();
      this.component.trigger(document, Pixelated.events.ui.tag.select, { tag: 'amazing'});

      expect(mailUncheckedEvent).toHaveBeenTriggeredOn(document);
      expect(checkbox.prop('checked')).toBe(false);
    });

    it('checkCheckbox checks it and triggers events.ui.mail.checked', function () {
      this.component.checkCheckbox();

      expect(checkbox.prop('checked')).toBe(true);
      expect(mailCheckedEvent).toHaveBeenTriggeredOn(document);
    });

    it('uncheckCheckbox checks it and triggers events.ui.mail.checked', function () {
      checkbox.prop('checked', true);
      this.component.uncheckCheckbox();

      expect(checkbox.prop('checked')).toBe(false);
      expect(mailUncheckedEvent).toHaveBeenTriggeredOn(document);
    });
  });
});
