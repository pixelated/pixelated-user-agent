define(
  [
    'flight/lib/component',
    'tags/ui/tag',
    'views/templates',
    'page/events',
    'tags/ui/tag_shortcut'
  ],

  function(defineComponent, Tag, templates, events, TagShortcut) {
    'use strict';

    var ICON_FOR = {
      'inbox': 'inbox',
      'sent': 'send',
      'drafts': 'pencil',
      'trash': 'trash-o',
      'all': 'archive'
    };

    var ORDER = {
      'inbox': '0',
      'sent': '1',
      'drafts': '2',
      'trash': '3',
      'all': '4'
    };

    return defineComponent(tagList);

    function tagOrder(nm) {
      return ORDER[nm.name] || '999' + nm.name;
    }

    function tagList() {
      this.defaultAttrs({
        defaultTagList: '#default-tag-list',
        customTagList: '#custom-tag-list'
      });

      this.renderShortcut = function (tag, tagComponent) {
        TagShortcut.appendedTo($('#tags-shortcuts'), { linkTo: tag, trigger: tagComponent});
      };

      function renderTag(tag, defaultList, customList) {
        var list = tag.default ? defaultList : customList;

        var tagComponent = Tag.appendedTo(list, {tag: tag});
        if (_.contains(_.keys(ORDER), tag.name)) {
          this.renderShortcut(tag, tagComponent);
        }
      }

      function resetTagList(lists) {
        _.each(lists, function (list) {
          this.trigger(list, events.tags.teardown);
          list.empty();
        }.bind(this));
      }

      this.renderTagList = function(tags) {
        var defaultList = this.select('defaultTagList');
        var customList = this.select('customTagList');

        resetTagList.bind(this, [defaultList, customList]).call();

        tags.forEach(function (tag) {
          renderTag.bind(this, tag, defaultList, customList).call();
        }.bind(this));
      };


      this.loadTagList = function(ev, data) {
        this.renderTagList(_.sortBy(data.tags, tagOrder));
        this.trigger(document, events.ui.tags.loaded, { tag: this.attr.currentTag });
      };

      this.saveTag = function(ev, data) {
        this.attr.currentTag = data.tag;
      };

      this.renderTagListTemplate = function () {
        this.$node.html(templates.tags.tagList());
      };

      this.after('initialize', function() {
        this.on(document, events.ui.tagList.load, this.loadTagList);
        this.on(document, events.ui.tag.selected, this.saveTag);
        this.renderTagListTemplate();
      });
    }
  }
);
