describeComponent('mail_view/ui/recipients/recipients_input',function () {
  'use strict';

  beforeEach(function () {
    this.setupComponent({name: 'to'});
    spyOn($, 'getJSON').and.returnValue($.Deferred());
  });

  describe('keys that finish address input', function () {

    _.each([
      [186, 'semicolon'],
      [188, 'comma'],

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

      it('wont add address if shift key is pressed together: ' + keycode[1], function () {
        var addressEnteredEvent = spyOnEvent(this.$node, Pixelated.events.ui.recipients.entered);

        var enterAddressKeyPressEvent = $.Event('keydown', { which: keycode[0], shiftKey: true });
        this.$node.val('a@b.c');
        this.$node.trigger(enterAddressKeyPressEvent);

        expect(addressEnteredEvent).not.toHaveBeenTriggeredOnAndWith(this, { name: 'to', address: 'a@b.c' });
      });

      it('prevents event default regardless on input val when key is ' + keycode[1], function () {
        var enterAddressKeyPressEvent = $.Event('keydown', { which: keycode[0] });
        spyOn(enterAddressKeyPressEvent, 'preventDefault');

        this.$node.val('');
        this.$node.trigger(enterAddressKeyPressEvent);
        expect(enterAddressKeyPressEvent.preventDefault).toHaveBeenCalled();

        enterAddressKeyPressEvent.preventDefault.calls.reset();
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

    describe('when space is pressed', function () {
      it('address input should not finish', function () {
        var addressEnteredEvent = spyOnEvent(this.$node, Pixelated.events.ui.recipients.entered);

        var spaceKeyPressEvent = $.Event('keydown', { which: 32});
        spyOn(spaceKeyPressEvent, 'preventDefault');

        this.$node.val('a@b.c');
        this.$node.trigger(spaceKeyPressEvent);

        expect(spaceKeyPressEvent.preventDefault).not.toHaveBeenCalled();
        expect(addressEnteredEvent).not.toHaveBeenTriggeredOnAndWith(this, { name: 'to', address: 'a@b.c' });
      });
    });
  });

  describe('on keyup', function () {
    it('triggers inputFieldIsEmpty if input is empty', function () {
      var inputFieldIsEmptyEvent = spyOnEvent(document, Pixelated.events.ui.recipients.inputFieldIsEmpty);
      this.$node.val('');

      this.$node.trigger('keyup');

      expect(inputFieldIsEmptyEvent).toHaveBeenTriggeredOn(document);
    });

    it('triggers inputFieldHasCharacters if input is not empty', function () {
      var inputFieldHasCharactersEvent = spyOnEvent(document, Pixelated.events.ui.recipients.inputFieldHasCharacters);
      this.$node.val('lalala');

      this.$node.trigger('keyup');

      expect(inputFieldHasCharactersEvent).toHaveBeenTriggeredOn(document, { name: 'to' });
    });
  });

  describe('on blur', function() {
    it('tokenizes and sanitize recipient email if there is an input val', function() {
      var addressEnteredEvent = spyOnEvent(this.$node, Pixelated.events.ui.recipients.entered);
      var blurEvent = $.Event('blur');
      spyOn(blurEvent, 'preventDefault');

      this.$node.val('a@b.c, Friend <friend@domain.com>; d@e.f  , , , , , , , ,');
      this.$node.trigger(blurEvent);

      expect(blurEvent.preventDefault).toHaveBeenCalled();
      expect(addressEnteredEvent.callCount).toEqual(3);

      expect(addressEnteredEvent.calls[0].data).toEqual({name: 'to', address: 'a@b.c'});
      expect(addressEnteredEvent.calls[1].data).toEqual({name: 'to', address: 'Friend <friend@domain.com>'});
      expect(addressEnteredEvent.calls[2].data).toEqual({name: 'to', address: 'd@e.f'});
    });
  });
});
