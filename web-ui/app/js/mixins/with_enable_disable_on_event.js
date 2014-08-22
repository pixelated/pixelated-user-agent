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

define([],
  function () {
    'use strict';

    function withEnableDisableOnEvent(ev) {
      return function () {
        this.disableElement = function () {
          this.$node.attr('disabled', 'disabled');
        };

        this.enableElement = function () {
          this.$node.removeAttr('disabled');
        };

        this.toggleEnabled = function (ev, enable) {
          if (enable) {
            this.enableElement();
          } else {
            this.disableElement();
          }
        };

        this.after('initialize', function () {
          this.on(document, ev, this.toggleEnabled);
        });
      };
    }

    return withEnableDisableOnEvent;
  }
);
