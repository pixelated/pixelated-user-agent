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

      this.renderTemplate = function (linkTo) {
        var model = {
          tagName: linkTo.name,
          displayBadge: this.displayBadge(linkTo),
          badgeType: this.badgeType(linkTo),
          count: this.badgeType(linkTo) === 'total' ? linkTo.counts.total : (linkTo.counts.total - linkTo.counts.read),
          icon: iconFor[linkTo.name]
        };
        return templates.tags.shortcut(model);
      };

      this.renderAndAttach = function (parent, options) {
        parent.append(this.renderTemplate(options.linkTo));
        this.initialize(parent.children().last(), options);
      };

      this.reRender = function () {
        this.$node.html(this.renderTemplate(this.attr.linkTo));
      };

      var iconFor = {
        'inbox': 'inbox',
        'sent': 'send',
        'drafts': 'pencil',
        'trash': 'trash-o',
        'all': 'archive'
      };

      this.selectTag = function (ev, data) {
        if (data.tag === this.attr.linkTo.name) {
          this.doSelect();
        }
        else {
          this.doUnselect();
        }
      };

      this.doUnselect = function () {
        this.$node.removeClass('selected');
      };

      this.doSelect = function () {
        this.$node.addClass('selected');
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
        this.on(document, events.ui.tag.select, this.selectTag);
        this.on(document, events.tags.shortcuts.teardown, this.doTeardown);
      });

    }
  }
);
