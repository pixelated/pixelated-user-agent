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
    'views/templates',
    'mixins/with_hide_and_show',
    'page/events'
  ],

  function(defineComponent, templates, withHideAndShow, events) {
    'use strict';

    //return defineComponent(noMailsAvailablePane, withHideAndShow);
    return defineComponent(noMailsAvailablePane);

    function noMailsAvailablePane() {
      this.defaultAttrs({
        tag: null,
        forSearch: ''
      });

      var mailsQueryMatch = /-?in:"?[\w]+"?|tag:"[\w]+"/g;

      this.render = function() {
        this.attr.tag = 'tags.' + this.attr.tag;
        this.attr.forSearch = this.attr.forSearch.replace(mailsQueryMatch, '').trim();
        this.$node.html(templates.noMailsAvailable(this.attr));
      };

      this.after('initialize', function () {
        this.render();
      });
    }
  }
);
