/*global Smail */

describeComponent('dispatchers/left_pane_dispatcher', function () {
  'use strict';

  describe('initialize', function () {
    it('asks for tags', function () {
      var tagWantEvent = spyOnEvent(document, Smail.events.tags.want);

      setupComponent();

      expect(tagWantEvent).toHaveBeenTriggeredOn(document);
      expect(tagWantEvent.mostRecentCall.data.caller[0]).toEqual(this.$node[0]);
    });
  });

  describe('after initialization', function () {
    beforeEach(function () {
      setupComponent();
    });

    it('pushes the url state when a tag is selected but not for the first tag', function () {
      var pushStateEvent = spyOnEvent(document, Smail.events.router.pushState);

      $(document).trigger(Smail.events.ui.tag.selected, { tag: 'Drafts'});
      $(document).trigger(Smail.events.ui.tag.selected, { tag: 'inbox'});

      expect(pushStateEvent).toHaveBeenTriggeredOn(document, { tag: 'inbox'});
    });

    it('fetches mails by tag when a tag is selected', function () {
      var fetchByTagEvent = spyOnEvent(document, Smail.events.ui.mails.fetchByTag);

      $(document).trigger(Smail.events.ui.tag.selected, { tag: 'Drafts'});

      expect(fetchByTagEvent).toHaveBeenTriggeredOn(document, { tag: 'Drafts'});
    });

    it('doesnt fetch mails by tag when skipMailListRefresh is sent on tag.selected', function () {
      var fetchByTagEvent = spyOnEvent(document, Smail.events.ui.mails.fetchByTag);

      $(document).trigger(Smail.events.ui.tag.selected, { tag: 'Drafts', skipMailListRefresh: true});

      expect(fetchByTagEvent).not.toHaveBeenTriggeredOn(document, { tag: 'Drafts'});
    });

    it('asks for more tags when refreshTagList is fired', function () {
      var tagWantEvent = spyOnEvent(document, Smail.events.tags.want);

      $(document).trigger(Smail.events.dispatchers.tags.refreshTagList);

      expect(tagWantEvent).toHaveBeenTriggeredOn(document);
    });

    it('fires tagLoad when the tags are received', function () {
      var tagListLoadEvent = spyOnEvent(document, Smail.events.ui.tagList.load);

      this.$node.trigger(Smail.events.tags.received, { tags: ['tags']});

      expect(tagListLoadEvent).toHaveBeenTriggeredOn(document, { tags: ['tags']});
    });

    it('on tags loaded selects the inbox tag if no data is provided', function () {
      var selectTagEvent = spyOnEvent(document, Smail.events.ui.tag.select);

      $(document).trigger(Smail.events.ui.tags.loaded);

      expect(selectTagEvent).toHaveBeenTriggeredOnAndWith(document, { tag: 'inbox' });
    });

    it('on tags loaded selects the a different tag if tag is provided', function () {
      var selectTagEvent = spyOnEvent(document, Smail.events.ui.tag.select);

      $(document).trigger(Smail.events.ui.tags.loaded, { tag: 'Drafts' });

      expect(selectTagEvent).toHaveBeenTriggeredOnAndWith(document, { tag: 'Drafts' });
    });
  });
});
