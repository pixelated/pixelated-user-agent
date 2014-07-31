describeComponent('tags/ui/tag_list', function () {
  'use strict';

  var tag = function(name, ident, def) {
    def = def || false;
    return {name: name, counts: {read: 0, total: 0, replied: 0, starred: 0}, ident: ident, default: def};
  };


  describe('post initialization', function() {
    beforeEach(function () {
      setupComponent();
    });

    it('should render tags when tagsList:load is received', function() {
      this.component.attr.default = false;
      var tagList = [tag('tag1', 1), tag('tag2', 2), tag('tag3', 3)];

      $(document).trigger(Smail.events.ui.tagList.load, {tags: tagList});

      var items = _.map(this.$node.find('li'), function(el) {
        return $(el).attr('id');
      });

      expect(items).toEqual(['tag-1', 'tag-2', 'tag-3']);
    });

    it('should render the default tags when tagsList:load is received and default attribute is true', function() {
      var tagList = [tag('tag1', 1, false), tag('tag2', 2, true), tag('tag3', 3, true)];

      $(document).trigger(Smail.events.ui.tagList.load, {tags: tagList});

      var items = _.map(this.component.select('defaultTagList').find('li'), function(el) {
        return $(el).attr('id');
      });

      expect(items).toEqual(['tag-2', 'tag-3']);
    });

    it('should render the custom tags when tagsList:load is received and default attribute is false', function() {
      var tagList = [tag('tag1', 1, false), tag('tag2', 2, true), tag('tag3', 3, true)];

      $(document).trigger(Smail.events.ui.tagList.load, {tags: tagList});

      var items = _.map(this.component.select('customTagList').find('li'), function(el) {
        return $(el).attr('id');
      });

      expect(items).toEqual(['tag-1']);
    });

    it('should trigger event to tell that tags were loaded sending the current tag', function () {
      this.component.attr.currentTag = 'Drafts';
      var tagsLoadedEvent = spyOnEvent(document, Smail.events.ui.tags.loaded);

      $(document).trigger(Smail.events.ui.tagList.load, {tags: [] });

      expect(tagsLoadedEvent).toHaveBeenTriggeredOnAndWith(document, { tag: 'Drafts'});
    });

    it('should send tag as undefined when tags are loaded and no tag was selected yet', function () {
      var tagsLoadedEvent = spyOnEvent(document, Smail.events.ui.tags.loaded);

      $(document).trigger(Smail.events.ui.tagList.load, {tags: [] });

      expect(tagsLoadedEvent).toHaveBeenTriggeredOnAndWith(document, { tag: undefined });
    });

    it('should save the current tag when a tag is selected', function () {
      $(document).trigger(Smail.events.ui.tag.selected, { tag: 'amazing'});

      expect(this.component.attr.currentTag).toEqual('amazing');
    });
  });
});
