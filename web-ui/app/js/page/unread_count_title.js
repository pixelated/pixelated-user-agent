/*
 * Copyright (c) 2015 ThoughtWorks, Inc.
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
    'page/events',
  ],

  function (defineComponent, events) {
    'use strict';

    return defineComponent(function () {
      this.getTitleText = function () {
        return document.title;
      };

      this.updateCount = function (ev, data) {
        var unread = data.mails.filter(function (mail) {
            return mail.status.indexOf('read') === -1;
        }).length;

        var tag = this.toTitleCase(data.tag);
        var counter = unread > 0 ? ' (' + unread + ') - ' : ' - ';
        document.title = tag + counter  + this.rawTitle;
      };

      this.toTitleCase = function (str) {
        return str.replace(/\b\w/g, function (txt) { return txt.toUpperCase(); });
      };

      this.after('initialize', function () {
        this.rawTitle = document.title;
        this.on(document, events.mails.available, this.updateCount);
      });

    });
});
