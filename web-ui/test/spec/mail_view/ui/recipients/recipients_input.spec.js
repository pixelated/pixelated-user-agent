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

      it('won`t add address if shift key is pressed together: ' + keycode[1], function () {
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

  describe('on focusout', function() {
    var addressEnteredEvent, focusoutEvent;

    beforeEach(function() {
      addressEnteredEvent = spyOnEvent(this.$node, Pixelated.events.ui.recipients.entered);
      focusoutEvent = $.Event('focusout');
      spyOn(focusoutEvent, 'preventDefault');
    });

    it('tokenizes and sanitize recipient email if there is an input val', function() {
      this.$node.val('a@b.c, Friend <friend@domain.com>; d@e.f  , , , , , , , ,');
      this.$node.trigger(focusoutEvent);

      expect(focusoutEvent.preventDefault).toHaveBeenCalled();
      expect(addressEnteredEvent.callCount).toEqual(3);

      expect(addressEnteredEvent.calls[0].data).toEqual({name: 'to', address: 'a@b.c'});
      expect(addressEnteredEvent.calls[1].data).toEqual({name: 'to', address: 'Friend <friend@domain.com>'});
      expect(addressEnteredEvent.calls[2].data).toEqual({name: 'to', address: 'd@e.f'});
    });

    it('tokenizes and sanitize adresses separated by space, comma and semicolon', function() {
      this.$node.val('a@b.c Friend <friend@domain.com>, d@e.f; g@h.i');
      this.$node.trigger(focusoutEvent);

      expect(focusoutEvent.preventDefault).toHaveBeenCalled();
      expect(addressEnteredEvent.callCount).toEqual(4);

      expect(addressEnteredEvent.calls[0].data).toEqual({name: 'to', address: 'a@b.c'});
      expect(addressEnteredEvent.calls[1].data).toEqual({name: 'to', address: 'Friend <friend@domain.com>'});
      expect(addressEnteredEvent.calls[2].data).toEqual({name: 'to', address: 'd@e.f'});
      expect(addressEnteredEvent.calls[3].data).toEqual({name: 'to', address: 'g@h.i'});
    });
  });

  describe('validate email format', function() {
    var invalidAddressEnteredEvent, addressEnteredEvent, focusoutEvent;

    beforeEach(function () {
      invalidAddressEnteredEvent = spyOnEvent(this.$node, Pixelated.events.ui.recipients.enteredInvalid);
      addressEnteredEvent = spyOnEvent(this.$node, Pixelated.events.ui.recipients.entered);
      focusoutEvent = $.Event('focusout');
      spyOn(focusoutEvent, 'preventDefault');
    });

    it('displays it as an invalid address token', function() {
      this.$node.val('invalid');
      this.$node.trigger(focusoutEvent);

      expect(focusoutEvent.preventDefault).toHaveBeenCalled();
      expect(invalidAddressEnteredEvent).toHaveBeenTriggeredOnAndWith(this, { name: 'to', address: 'invalid' });
    });

    it('displays it as an invalid address token when cannot parse', function() {
      this.$node.val('invalid_format, email@example.com');
      this.$node.trigger(focusoutEvent);

      expect(focusoutEvent.preventDefault).toHaveBeenCalled();
      expect(invalidAddressEnteredEvent.calls[0].data).toEqual({name: 'to', address: 'invalid_format'});
      expect(addressEnteredEvent.calls[0].data).toEqual({name: 'to', address: 'email@example.com'});
    });

    it('displays it as an invalid address token when domain isn`t complete', function() {
      this.$node.val('email@example');
      this.$node.trigger(focusoutEvent);

      expect(focusoutEvent.preventDefault).toHaveBeenCalled();
      expect(invalidAddressEnteredEvent.calls[0].data).toEqual({name: 'to', address: 'email@example'});
    });

    it('displays it as an invalid address token when cannonical email domain isn`t complete', function() {
      this.$node.val('Invalid <email@example>');
      this.$node.trigger(focusoutEvent);

      expect(focusoutEvent.preventDefault).toHaveBeenCalled();
      expect(invalidAddressEnteredEvent.calls[0].data).toEqual({name: 'to', address: 'Invalid <email@example>'});
    });

    it('parses email with dash' , function() {
      this.$node.val('team@pixelated-project.org');
      this.$node.trigger(focusoutEvent);

      expect(focusoutEvent.preventDefault).toHaveBeenCalled();
      expect(addressEnteredEvent.calls[0].data).toEqual({name: 'to', address: 'team@pixelated-project.org'});
    });

    it('parses cannonical email with dash' , function() {
      this.$node.val('Pixelated <team@pixelated-project.org>');
      this.$node.trigger(focusoutEvent);

      expect(focusoutEvent.preventDefault).toHaveBeenCalled();
      expect(addressEnteredEvent.calls[0].data).toEqual({name: 'to', address: 'Pixelated <team@pixelated-project.org>'});
    });
 });
});
