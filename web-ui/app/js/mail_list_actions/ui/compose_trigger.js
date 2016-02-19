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
    'page/events'
  ],

  function(defineComponent, templates, events) {
    'use strict';

    return defineComponent(composeTrigger);

    function composeTrigger() {

      this.defaultAttrs({});

      this.render = function() {
        this.$node.html(templates.mailActions.composeTrigger);
      };

      this.enableComposing = function(event, data) {
        this.trigger(document, events.dispatchers.rightPane.openComposeBox);
      };

      this.showEmailSuccess = function () {
        this.trigger(document, events.ui.userAlerts.displayMessage, {message: 'Your message was sent!', class: 'success'});
      };

      this.showEmailError = function (ev, data) {
        this.trigger(document, events.ui.userAlerts.displayMessage, {message: 'Error,  message not sent: ' + data.responseJSON.message, class: 'error'});
      };

      this.after('initialize', function () {
        this.render();
        this.on('click', this.enableComposing);
        this.on(document, events.mail.sent, this.showEmailSuccess);
        this.on(document, events.mail.send_failed, this.showEmailError);
      });
    }
  }
);
