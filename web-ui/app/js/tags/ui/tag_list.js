/*
 * Copyright (c) 2014 ThoughtWorks, Inc.
 *
 * Pixelated is free software: you can redistribute it and/or modify
 * it under the terms of the GNU Affero General Public License as published by
 * the Free Software Foundation, either version 3 of the License, or
 * (at your option) any later version.
 *
 * Pixelated is distributed in the hope that it will be useful,
 * but WITHOUT ANY WARRANTY; without even the implied warranty of
 * MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
 * GNU Affero General Public License for more details.
 *
 * You should have received a copy of the GNU Affero General Public License
 * along with Pixelated. If not, see <http://www.gnu.org/licenses/>.
 */
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
        return TagShortcut.appendedTo($('#tags-shortcuts'), { linkTo: tag, trigger: tagComponent});
      };

      function renderTag(tag, defaultList, customList) {
        var list = tag.default ? defaultList : customList;

        var tagComponent = Tag.appendedTo(list, {tag: tag});
        if (_.contains(_.keys(ORDER), tag.name)) {
          tagComponent.attr.shortcut = this.renderShortcut(tag, tagComponent);
        }
      }

      function resetTagList(lists) {
        _.each(lists, function (list) {
          this.trigger(list, events.tags.teardown);
          list.empty();
        }.bind(this));

      }

      this.resetShortcuts = function () {
        $('#tags-shortcuts').empty();
        this.trigger(document, events.tags.shortcuts.teardown);
      };

      this.renderTagList = function(tags) {
        var defaultList = this.select('defaultTagList');
        var customList = this.select('customTagList');

        resetTagList.bind(this, [defaultList, customList]).call();
        this.resetShortcuts();

        tags.forEach(function (tag) {
          renderTag.bind(this, tag, defaultList, customList).call();
        }.bind(this));
      };

      this.loadTagList = function(ev, data) {
        this.renderTagList(_.sortBy(data.tags, tagOrder));
        this.trigger(document, events.ui.tags.loaded, { tag: this.attr.currentTag, skipMailListRefresh: data.skipMailListRefresh});
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
