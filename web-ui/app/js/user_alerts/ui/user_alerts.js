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

    return defineComponent(userAlerts, withHideAndShow);

    function userAlerts() {
      this.defaultAttrs({
        dismissTimeout: 3000
      });

      this.render = function(message) {
        this.$node.html(templates.userAlerts.message(message));
        this.show();
        setTimeout(this.hide.bind(this), this.attr.dismissTimeout);
      };


      this.displayMessage = function(ev, data) {
        this.render({
          message: {
            content: data.message,
            class: 'message-panel__growl--' + (data.class || 'success')
          }
        });
      };

      this.after('initialize', function() {
        this.on(document, events.ui.userAlerts.displayMessage, this.displayMessage);
      });
    }
  }
);

