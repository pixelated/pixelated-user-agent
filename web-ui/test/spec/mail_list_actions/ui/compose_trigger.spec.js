describeComponent('mail_list_actions/ui/compose_trigger', function () {
  'use strict';

  beforeEach(function () {
    setupComponent('<div></div>');
  });

  it('triggers the enableComposebox event when clicked', function () {
    var spyEvent = spyOnEvent(document, Pixelated.events.dispatchers.rightPane.openComposeBox);

    this.component.trigger('click');

    expect(spyEvent).toHaveBeenTriggeredOn(document);
  });

});
