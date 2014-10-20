/*global jasmine */
/*global Pixelated */

describeComponent('search/search_trigger', function () {
  'use strict';
  var self;

  beforeEach(function () {
    this.setupComponent();
    self = this;
  });

  function submitSearch(queryString) {
    self.component.select('input').val(queryString);
    self.component.select('form').submit();
  }

  it('should trigger search when the submit occurs', function () {
    var spy = spyOnEvent(document, Pixelated.events.search.perform);

    submitSearch('tanana');
    expect(spy).toHaveBeenTriggeredOnAndWith(document, { query: 'tanana' });
  });

  it('should select the "all" tag when submit occurs but should skip mail list refresh', function  (){
    var tagSelectEvent = spyOnEvent(document, Pixelated.events.ui.tag.select);

    submitSearch('tanana');

    expect(tagSelectEvent).toHaveBeenTriggeredOnAndWith(document, {
      tag: 'all',
      skipMailListRefresh: true
    });
  });

  it('should select the "all" tag when an empty submit occurs and shoud refresh mail list', function() {
    var tagSelectEvent = spyOnEvent(document, Pixelated.events.ui.tag.select);
    var emptySearchEvent = spyOnEvent(document, Pixelated.events.search.empty);

    submitSearch('');

    expect(emptySearchEvent).toHaveBeenTriggeredOn(document);
    expect(tagSelectEvent).toHaveBeenTriggeredOnAndWith(document, { tag: 'all'});

  });

  it('should clear input when selecting a new tag', function(){
    submitSearch('tanana');
    $(document).trigger(Pixelated.events.ui.tag.selected, { tag: 'inbox'});
    expect(self.component.select('input').val()).toBe('');
  });

  it('should add place holder on input value after doing a search', function(){
    submitSearch('teste');
    expect(self.component.select('input').val()).toBe('Search results for: teste');
  });

  it('should remove place holder on input value when input is on focus', function(){
    submitSearch('teste');
    this.component.select('input').focus();
    expect(self.component.select('input').val()).toBe('teste');
  });

  it('should remove place holder on input value when input is not on focus', function(){
    submitSearch('teste');
    this.component.select('input').focus();
    this.component.select('input').blur();
    expect(self.component.select('input').val()).toBe('Search results for: teste');
  });

  it('should not change input value when input is empty', function(){
    submitSearch('');
    this.component.select('input').focus();
    expect(self.component.select('input').val()).toBe('');
  });


});
