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
    'flight/lib/component'
  ],

  function (defineComponent) {
    'use strict';

    return defineComponent(mailSyncingProgressbar);

    function mailSyncingProgressbar() {
      this.updateProgressBar = function (count) {
        this.attr.syncingMails = true;

        this.$node.css({
          'width': (count.progress * 100).toFixed(2) + '%',
          'transition': '1000ms linear',
          'background-color': '#FF7902',
          'height': '3px'
        });

      };

      this.resetProgressBar = function () {
        this.$node.removeAttr('style');
        this.attr.syncingMails = false;
        clearInterval(this.attr.updateIntervalId);
      };

      this.doUpdate = function () {
        $.getJSON('/sync_info')
          .success(function (data) {
            if (data.is_syncing) {
              this.updateProgressBar(data.count);
            } else {
              this.resetProgressBar();
            }
          }.bind(this))
          .error(function () {
            clearInterval(this.attr.poolIntervalId);
            this.resetProgressBar();
          }.bind(this));
      };

      this.checkForMailSyncing = function () {
        if (this.attr.syncingMails) {
          return;
        }
        this.attr.updateIntervalId = setInterval(this.doUpdate.bind(this), 1000);
      };

      this.after('initialize', function () {
        this.checkForMailSyncing();
        this.attr.poolIntervalId = setInterval(this.checkForMailSyncing.bind(this), 20000);
      });
    }
  }
);
