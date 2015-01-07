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
/*global Pixelated */
/*global _ */

define(['features'],
  function (features) {
    'use strict';

    function withAutoRefresh(refreshMethod) {
      return function () {
        this.defaultAttrs({
          refreshInterval: 15000
        });

        this.setupRefresher = function () {
          clearTimeout(this.attr.refreshTimer);
          this.attr.refreshTimer = setTimeout(function () {
            this[refreshMethod]();
            this.setupRefresher();
          }.bind(this), this.attr.refreshInterval);
        };

        this.after('initialize', function () {
          if (features.isAutoRefreshEnabled()) {
            this.setupRefresher();
          }
        });
      };
    }

    return withAutoRefresh;
  }
);

