/* global Smail */

describeComponent('mail_view/ui/recipients/recipients',function () {
  'use strict';
  var recipientsUpdatedEvent;

  describe('initialization', function() {
    it('adds recipients', function() {
      setupComponent({name: 'to', addresses: ['foobar@gmail.com'] });
      expect(this.component.attr.recipients.length).toBe(1);
    });

    it('does not trigger recipients updated events on initialization', function() {
      recipientsUpdatedEvent = spyOnEvent(document, Smail.events.ui.recipients.updated);

      setupComponent({name: 'to', addresses: ['foobar@gmail.com'] });
      expect(recipientsUpdatedEvent).not.toHaveBeenTriggeredOn(document);
    });
  });

  describe('adding recipients from the ui', function() {
    beforeEach(function () {
      setupComponent();
      recipientsUpdatedEvent  = spyOnEvent(document, Smail.events.ui.recipients.updated);
      this.component.trigger(Smail.events.ui.recipients.entered, {name: 'to', addresses: ['foobar@gmail.com'] });
    });

    it('triggers recipients updated', function() {
      expect(recipientsUpdatedEvent).toHaveBeenTriggeredOn(document);
    });

    it('adds recipients', function() {
      expect(this.component.attr.recipients.length).toBe(1);
    });
  });
});
