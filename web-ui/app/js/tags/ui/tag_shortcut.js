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
'use strict';
define(
  [
    'flight/lib/component',
    'views/templates',
    'page/events',
    'tags/ui/tag_base',
    'flight/lib/utils'
  ],

  function (describeComponent, templates, events, tagBase, utils) {

    var TagShortcut = describeComponent(tagShortcut, tagBase);

    TagShortcut.appendedTo = function (parent, data) {
      var res = new this();
      res.renderAndAttach(parent, data);
      return res;
    };

    return TagShortcut;

    function tagShortcut() {

      this.renderTemplate = function (tag, currentTag) {
        var model = {
          tagName: tag.name,
          displayBadge: this.displayBadge(tag),
          badgeType: this.badgeType(tag),
          count: this.badgeType(tag) === 'total' ? tag.counts.total : (tag.counts.total - tag.counts.read),
          icon: iconFor[tag.name],
          selected: tag.name === currentTag ? 'selected' : ''
        };
        return templates.tags.shortcut(model);
      };

      this.renderAndAttach = function (parent, options) {
        parent.append(this.renderTemplate(options.tag, options.currentTag));
        this.initialize(parent.children().last(), options);
      };

      this.reRender = function () {
        this.$node.html(this.renderTemplate(this.attr.tag, this.attr.currentTag));
      };

      var iconFor = {
        'inbox': 'inbox',
        'sent': 'send',
        'drafts': 'pencil',
        'trash': 'trash-o',
        'all': 'archive'
      };

      this.doTeardown = function () {
        if (!jQuery.contains(document, this.$node[0])) {
          this.teardown();
        }
      };

      this.after('initialize', function () {
        this.on('click', function () {
          this.attr.trigger.triggerSelect();
        });
        this.on(document, events.tags.shortcuts.teardown, this.doTeardown);
      });

    }
  }
);
