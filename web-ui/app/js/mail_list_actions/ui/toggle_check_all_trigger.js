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
    'page/events'
  ],

  function(defineComponent, events) {
    'use strict';

    return defineComponent(toggleCheckAllEmailsTrigger);

    function toggleCheckAllEmailsTrigger() {
      this.defaultAttrs({ });

      this.toggleCheckAll = function(event) {
        if (this.$node.prop('checked')) {
          this.trigger(document, events.ui.mails.checkAll);
        } else {
          this.trigger(document, events.ui.mails.uncheckAll);
        }
      };

      this.setCheckbox = function (event, state) {
        this.$node.prop('checked', state);
      };

      this.after('initialize', function () {
        this.on('click', this.toggleCheckAll);
        this.on(document, events.ui.mails.hasMailsChecked, this.setCheckbox);
      });
    }
  }
);
