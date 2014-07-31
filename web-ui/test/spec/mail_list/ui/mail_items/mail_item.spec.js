/*global Smail */

describeMixin('mail_list/ui/mail_items/mail_item', function () {
  'use strict';

  beforeEach(function () {
    var mail = Smail.testData().parsedMail.simpleTextPlain;
    mail.tags = ['inbox'];

    setupComponent('<li><input type="checkbox"></input></li>', {
      mail: mail,
      selected: false,
      tag: 'inbox'
    });
  });

  describe('mail checkbox', function () {
    var mailCheckedEvent, mailUncheckedEvent, checkbox;
    beforeEach(function () {
      mailCheckedEvent = spyOnEvent(document, Smail.events.ui.mail.checked);
      mailUncheckedEvent = spyOnEvent(document, Smail.events.ui.mail.unchecked);
      checkbox = this.component.$node.find('input[type=checkbox]');
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
