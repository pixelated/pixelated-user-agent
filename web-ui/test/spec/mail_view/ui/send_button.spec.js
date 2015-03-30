/* global Pixelated */

describeComponent('mail_view/ui/send_button', function () {

  'use strict';

  describe('send button', function () {
    beforeEach(function () {
      this.setupComponent('<button></button>');
    });

    describe('when it is disabled', function () {
      beforeEach(function () {
        this.$node.prop('disabled', true);
      });

      it('gets enabled in a inputFieldHasCharacters event', function () {
        $(document).trigger(Pixelated.events.ui.recipients.inputFieldHasCharacters, { name: 'to' });

        expect(this.$node).not.toBeDisabled();
      });

      it('gets enabled in a recipients:updated where there are new recipients', function () {
        $(document).trigger(Pixelated.events.ui.recipients.updated, { newRecipients: ['a@b.c']});

        expect(this.$node).not.toBeDisabled();
      });
    });

    describe('multiple events', function () {
      it('gets enabled and remains enabled when a inputFieldHasCharacters is followed by a recipients:updated with NO new recipients', function () {
        this.$node.prop('disabled', true);

        $(document).trigger(Pixelated.events.ui.recipients.inputFieldHasCharacters, { name: 'to' });
        $(document).trigger(Pixelated.events.ui.recipients.updated, { newRecipients: [] });

        expect(this.$node).not.toBeDisabled();
      });

      it('gets enabled and remains enabled when a recipients:updated with recipients is followed by a inputFieldIsEmpty', function () {
        this.$node.prop('disabled', true);

        $(document).trigger(Pixelated.events.ui.recipients.updated, { newRecipients: ['a@b.c']});
        $(document).trigger(Pixelated.events.ui.recipients.inputFieldIsEmpty, { name: 'to' });

        expect(this.$node).not.toBeDisabled();
      });
    });

    describe('when it is enabled', function () {
      beforeEach(function () {
        this.$node.prop('disabled', false);
      });

      it('gets disabled in a inputFieldIsEmpty', function () {
        $(document).trigger(Pixelated.events.ui.recipients.inputFieldIsEmpty, { name: 'to' });

        expect(this.$node).toBeDisabled();
      });

      it('gets disabled in a recipients:updated without new recipients', function () {
        $(document).trigger(Pixelated.events.ui.recipients.updated, { newRecipients: []});

        expect(this.$node).toBeDisabled();
      });

      it('gets disabled if recipients:updated with invalid email', function () {
        $(document).trigger(Pixelated.events.ui.recipients.inputFieldHasCharacters, { name: 'to' });
        $(document).trigger(Pixelated.events.ui.recipients.updated, { newRecipients: ['InvalidEmail']});

        expect(this.$node).not.toBeDisabled();
        expect(this.$node.text()).toBe('Send');
      });
    });

    describe('on click', function () {

      it ('asks for the recipients input to complete its current input', function () {
        var doCompleteInputEvent = spyOnEvent(document, Pixelated.events.ui.recipients.doCompleteInput);

        this.$node.click();

        expect(doCompleteInputEvent).toHaveBeenTriggeredOn(document);
      });

      it('disables the button after clicking', function () {
        expect(this.$node.text()).toBe('Send');

        this.$node.click();

        expect(this.$node.text()).toBe('Sending...');
        expect(this.$node.prop('disabled')).toBeTruthy();
      });

      it('enables again if sending errors out', function() {
        expect(this.$node.text()).toBe('Send');

        this.$node.click();

        $(document).trigger(Pixelated.events.mail.send_failed);

        expect(this.$node.text()).toBe('Send');
        expect(this.$node.prop('disabled')).not.toBeTruthy();

      });
    });

    describe('after clicking', function () {
      beforeEach(function () {
        this.$node.click();
      });

      it('waits for ui:mail:recipientsUpdated to happen 3 times in the mail then sends the mail then stops listening to ui:mail:recipientsUpdated', function () {
        var sendMailEvent = spyOnEvent(document, Pixelated.events.ui.mail.send);
        spyOn(this.component, 'off');

        _.times(3, function () { $(document).trigger(Pixelated.events.ui.mail.recipientsUpdated); });

        expect(sendMailEvent).toHaveBeenTriggeredOn(document);
        expect(this.component.off).toHaveBeenCalledWith(document, Pixelated.events.ui.mail.recipientsUpdated);
      });
    });
  });
});
