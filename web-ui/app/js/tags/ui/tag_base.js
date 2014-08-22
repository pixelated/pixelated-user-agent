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
define(['views/i18n', 'page/events'], function(i18n, events) {

  function tagBase() {
    var ALWAYS_HIDE_BADGE_FOR = ['sent', 'trash', 'all'];
    var TOTAL_BADGE = ['drafts'];

    this.displayBadge = function(tag) {
      if(_.include(ALWAYS_HIDE_BADGE_FOR, tag.name)) { return false; }
      if(this.badgeType(tag) === 'total') {
        return tag.counts.total > 0;
      } else {
        return (tag.counts.total - tag.counts.read) > 0;
      }
    };

    this.badgeType = function(tag) {
      return _.include(TOTAL_BADGE, tag.name) ? 'total' : 'unread';
    };

  }

  return tagBase;

});
