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
    'mixins/with_enable_disable_on_event',
    'page/events'
  ],

  function(defineComponent, templates, withEnableDisableOnEvent, events) {
    'use strict';

    return defineComponent(recoverManyTrigger, withEnableDisableOnEvent(events.ui.mails.hasMailsChecked));

    function recoverManyTrigger() {
      this.defaultAttrs({});

      this.getMailsToRecover = function(event) {
        this.trigger(document, events.ui.mail.wantChecked, this.$node);
      };

      this.recoverManyEmails = function (event, data) {
        this.trigger(document, events.ui.mail.recoverMany, data);
      };

      this.after('initialize', function () {
        this.on('click', this.getMailsToRecover);
        this.on(events.ui.mail.hereChecked, this.recoverManyEmails);
      });
    }
  }
);
