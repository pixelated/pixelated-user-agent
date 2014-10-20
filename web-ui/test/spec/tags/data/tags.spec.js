/* global Pixelated */

describeComponent('tags/data/tags', function () {
  'use strict';

  beforeEach(function () {
    this.setupComponent();
  });

  it('asks the server for tags when receiving the tags:want event', function() {
    spyOn($, 'ajax').and.returnValue({done: function() {}});

    this.component.trigger(Pixelated.events.tags.want);

    expect($.ajax.calls.mostRecent().args[0]).toEqual('/tags');
  });

  it('triggers an event on the initial sender after receiving tags', function() {
    var f;
    spyOn($, 'ajax').and.returnValue({done: function(d) { f = d; }});
    var me = {};
    var eventSpy = spyOnEvent(me, Pixelated.events.tags.received);

    this.component.trigger(Pixelated.events.tags.want, { caller: me});

    f(['foo', 'bar', 'quux/bar']);
    expect(eventSpy).toHaveBeenTriggeredOn(me);
  });

  it('triggers an event containing the returned tags', function() {
    var f;
    spyOn($, 'ajax').and.returnValue({done: function(d) { f = d; }});
    var me = {};
    var eventSpy = spyOnEvent(me, Pixelated.events.tags.received);
    this.component.trigger(Pixelated.events.tags.want, { caller: me });
    var tags = ['foo', 'bar', 'quux/bar'];
    f(tags);
    tags.push(this.component.all);
    expect(eventSpy.mostRecentCall.data).toEqual(jasmine.objectContaining({tags: tags}));
  });
});
