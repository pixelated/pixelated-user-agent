/* global Pixelated */

describeComponent('mail_view/ui/recipients/recipients',function () {
  'use strict';
  var recipientsUpdatedEvent;

  beforeEach(function () {
    spyOn($, 'getJSON').and.returnValue($.Deferred());
  });

  describe('initialization', function() {
    it('adds recipients', function() {
      this.setupComponent({name: 'to', addresses: ['foobar@gmail.com'] });
      expect(this.component.attr.recipients.length).toBe(1);
    });

    it('does not trigger recipients updated events on initialization', function() {
      recipientsUpdatedEvent = spyOnEvent(document, Pixelated.events.ui.recipients.updated);

      this.setupComponent({name: 'to', addresses: ['foobar@gmail.com'] });
      expect(recipientsUpdatedEvent).not.toHaveBeenTriggeredOn(document);
    });
  });

  describe('adding recipients from the ui', function() {
    beforeEach(function () {
      this.setupComponent();
      recipientsUpdatedEvent  = spyOnEvent(document, Pixelated.events.ui.recipients.updated);
    });

    it('triggers recipients updated', function() {
      this.component.trigger(Pixelated.events.ui.recipients.entered, {name: 'to', addresses: ['foobar@gmail.com'] });
      expect(recipientsUpdatedEvent).toHaveBeenTriggeredOn(document);
    });

    it('adds recipients', function() {
      this.component.trigger(Pixelated.events.ui.recipients.entered, {name: 'to', addresses: ['foobar@gmail.com'] });
      expect(this.component.attr.recipients.length).toBe(1);
    });
  });

  describe('adding invalid recipients from the ui', function() {
    beforeEach(function () {
      this.setupComponent();
      recipientsUpdatedEvent  = spyOnEvent(document, Pixelated.events.ui.recipients.updated);
      this.component.trigger(Pixelated.events.ui.recipients.enteredInvalid, {name: 'to', addresses: ['invalid.com'] });
    });

    it('does not trigger recipients updated', function() {
      expect(recipientsUpdatedEvent).not.toHaveBeenTriggeredOn(document);
    });

    it('adds recipients with invalid indication', function() {
      expect(this.component.attr.recipients.length).toBe(1);
      expect(this.component.attr.recipients[0].attr.invalidAddress).toBe(true);
    });
  });

});
