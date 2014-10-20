/*global Pixelated */

describeComponent('dispatchers/left_pane_dispatcher', function () {
  'use strict';

  describe('initialize', function () {
    it('asks for tags', function () {
      var tagWantEvent = spyOnEvent(document, Pixelated.events.tags.want);

      this.setupComponent();

      expect(tagWantEvent).toHaveBeenTriggeredOn(document);
      expect(tagWantEvent.mostRecentCall.data.caller[0]).toEqual(this.$node[0]);
    });
  });

  describe('after initialization', function () {
    beforeEach(function () {
      this.setupComponent();
    });

    it('pushes the url state when a tag is selected but not for the first tag', function () {
      var pushStateEvent = spyOnEvent(document, Pixelated.events.router.pushState);

      $(document).trigger(Pixelated.events.ui.tag.selected, { tag: 'Drafts'});
      $(document).trigger(Pixelated.events.ui.tag.selected, { tag: 'inbox'});

      expect(pushStateEvent).toHaveBeenTriggeredOn(document, { tag: 'inbox'});
    });

    it('fetches mails by tag when a tag is selected', function () {
      var fetchByTagEvent = spyOnEvent(document, Pixelated.events.ui.mails.fetchByTag);

      $(document).trigger(Pixelated.events.ui.tag.selected, { tag: 'Drafts'});

      expect(fetchByTagEvent).toHaveBeenTriggeredOn(document, { tag: 'Drafts'});
    });

    it('doesnt fetch mails by tag when skipMailListRefresh is sent on tag.selected', function () {
      var fetchByTagEvent = spyOnEvent(document, Pixelated.events.ui.mails.fetchByTag);

      $(document).trigger(Pixelated.events.ui.tag.selected, { tag: 'Drafts', skipMailListRefresh: true});

      expect(fetchByTagEvent).not.toHaveBeenTriggeredOn(document, { tag: 'Drafts'});
    });

    it('asks for more tags when refreshTagList is fired', function () {
      var tagWantEvent = spyOnEvent(document, Pixelated.events.tags.want);

      $(document).trigger(Pixelated.events.dispatchers.tags.refreshTagList, {});

      expect(tagWantEvent).toHaveBeenTriggeredOn(document);
    });

    it('fires tagLoad when the tags are received', function () {
      var tagListLoadEvent = spyOnEvent(document, Pixelated.events.ui.tagList.load);

      this.$node.trigger(Pixelated.events.tags.received, { tags: ['tags']});

      expect(tagListLoadEvent).toHaveBeenTriggeredOn(document, { tags: ['tags']});
    });

    it('on tags loaded selects the inbox tag if no data is provided', function () {
      var selectTagEvent = spyOnEvent(document, Pixelated.events.ui.tag.select);

      $(document).trigger(Pixelated.events.ui.tags.loaded, {});

      expect(selectTagEvent).toHaveBeenTriggeredOnAndWith(document, { tag: 'inbox' });
    });

    it('on tags loaded selects the a different tag if tag is provided', function () {
      var selectTagEvent = spyOnEvent(document, Pixelated.events.ui.tag.select);

      $(document).trigger(Pixelated.events.ui.tags.loaded, { tag: 'Drafts' });

      expect(selectTagEvent).toHaveBeenTriggeredOnAndWith(document, { tag: 'Drafts' });
    });
  });
});
