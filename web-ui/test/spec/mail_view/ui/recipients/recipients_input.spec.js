describeComponent('mail_view/ui/recipients/recipients_input',function () {
  'use strict';

  beforeEach(function () {
    setupComponent({name: 'to'});
  });

  describe('keys that finish address input', function () {

    _.each([
      [186, 'semicolon'],
      [188, 'comma'],
      [32, 'space']

    ], function (keycode) {

      it(': ' + keycode[1], function () {
        var addressEnteredEvent = spyOnEvent(this.$node, Pixelated.events.ui.recipients.entered);

        var enterAddressKeyPressEvent = $.Event('keydown', { which: keycode[0] });
        this.$node.val('a@b.c');
        this.$node.trigger(enterAddressKeyPressEvent);

        expect(addressEnteredEvent).toHaveBeenTriggeredOnAndWith(this, { name: 'to', address: 'a@b.c' });
      });

      it('wont add address if val is empty: ' + keycode[1], function () {
        var addressEnteredEvent = spyOnEvent(this.$node, Pixelated.events.ui.recipients.entered);

        var enterAddressKeyPressEvent = $.Event('keydown', { which: keycode[0] });
        this.$node.val('');
        this.$node.trigger(enterAddressKeyPressEvent);

        expect(addressEnteredEvent).not.toHaveBeenTriggeredOnAndWith(this, { name: 'to', address: '' });
      });

      it('prevents event default regardless on input val when key is ' + keycode[1], function () {
        var enterAddressKeyPressEvent = $.Event('keydown', { which: keycode[0] });
        spyOn(enterAddressKeyPressEvent, 'preventDefault');

        this.$node.val('');
        this.$node.trigger(enterAddressKeyPressEvent);
        expect(enterAddressKeyPressEvent.preventDefault).toHaveBeenCalled();

        enterAddressKeyPressEvent.preventDefault.reset();
        this.$node.val('anything');
        this.$node.trigger(enterAddressKeyPressEvent);
        expect(enterAddressKeyPressEvent.preventDefault).toHaveBeenCalled();
      });

    });

    describe('when tab is pressed', function () {
      it('enters an address and prevents event default if there is an input val', function () {
        var addressEnteredEvent = spyOnEvent(this.$node, Pixelated.events.ui.recipients.entered);

        var tabKeyPressEvent = $.Event('keydown', { which: 9});
        spyOn(tabKeyPressEvent, 'preventDefault');

        this.$node.val('a@b.c');
        this.$node.trigger(tabKeyPressEvent);

        expect(tabKeyPressEvent.preventDefault).toHaveBeenCalled();
        expect(addressEnteredEvent).toHaveBeenTriggeredOnAndWith(this, { name: 'to', address: 'a@b.c'});
      });

      it('doesnt enter an address and doesnt prevent event default if input val is empty (so tab moves it to the next input)', function () {
        var addressEnteredEvent = spyOnEvent(this.$node, Pixelated.events.ui.recipients.entered);

        var tabKeyPressEvent = $.Event('keydown', { which: 9});
        spyOn(tabKeyPressEvent, 'preventDefault');

        this.$node.val('');
        this.$node.trigger(tabKeyPressEvent);

        expect(tabKeyPressEvent.preventDefault).not.toHaveBeenCalled();
        expect(addressEnteredEvent).not.toHaveBeenTriggeredOnAndWith(this, { name: 'to', address: ''});
      });
    });
  });

  describe('on keyup', function () {
    it('triggers inputHasNoMail if input is empty', function () {
      var inputHasNoMailEvent = spyOnEvent(document, Pixelated.events.ui.recipients.inputHasNoMail);
      this.$node.val('');

      this.$node.trigger('keyup');

      expect(inputHasNoMailEvent).toHaveBeenTriggeredOn(document);
    });

    it('triggers inputHasMail if input is not empty', function () {
      var inputHasMailEvent = spyOnEvent(document, Pixelated.events.ui.recipients.inputHasMail);
      this.$node.val('lalala');

      this.$node.trigger('keyup');

      expect(inputHasMailEvent).toHaveBeenTriggeredOn(document, { name: 'to' });
    });
  });

});
