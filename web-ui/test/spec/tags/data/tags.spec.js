describeComponent('tags/data/tags', function () {
  'use strict';

  beforeEach(function () {
    setupComponent();
  });

  it('asks the server for tags when receiving the tags:want event', function() {
    spyOn($, 'ajax').andReturn({done: function() {}});

    this.component.trigger(Smail.events.tags.want);

    expect($.ajax.mostRecentCall.args[0]).toEqual('/tags');
  });

  it('triggers an event on the initial sender after receiving tags', function() {
    var f;
    spyOn($, 'ajax').andReturn({done: function(d) { f = d; }});
    var me = {};
    var eventSpy = spyOnEvent(me, Smail.events.tags.received);

    this.component.trigger(Smail.events.tags.want, { caller: me});

    f(['foo', 'bar', 'quux/bar']);
    expect(eventSpy).toHaveBeenTriggeredOn(me);
  });

  it('triggers an event containing the returned tags', function() {
    var f;
    spyOn($, 'ajax').andReturn({done: function(d) { f = d; }});
    var me = {};
    var eventSpy = spyOnEvent(me, Smail.events.tags.received);
    this.component.trigger(Smail.events.tags.want, { caller: me });
    var tags = ['foo', 'bar', 'quux/bar'];
    f(tags);
    tags.push(this.component.all);
    expect(eventSpy.mostRecentCall.data).toEqual({tags: tags});
  });
});
