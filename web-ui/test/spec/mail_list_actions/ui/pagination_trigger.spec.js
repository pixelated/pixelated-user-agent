describeComponent('mail_list_actions/ui/pagination_trigger', function () {
  'use strict';

  beforeEach(function () {
    setupComponent();
  });

  it('triggers the ui:page:previous event when the left arrow is clicked', function () {
    var eventSpy = spyOnEvent(document, Smail.events.ui.page.previous);
    this.component.select('previous').click();
    expect(eventSpy).toHaveBeenTriggeredOn(document);
  });


  it('triggers the ui:page:next event when the right arrow is clicked', function () {
    var eventSpy = spyOnEvent(document, Smail.events.ui.page.next);
    this.component.select('next').click();
    expect(eventSpy).toHaveBeenTriggeredOn(document);
  });

  it('re-renders with current page number when page changes', function () {
    this.component.trigger(document, Smail.events.ui.page.changed, {currentPage: 0});

    expect(this.component.select('currentPage').text()).toBe('1');
  });
});
