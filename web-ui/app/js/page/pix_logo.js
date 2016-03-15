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

    return defineComponent(pixLogo);

    function pixLogo() {
      this.turnAnimationOn = function () {
        $('.logo-part-animation-off').attr('class', 'logo-part-animation-on');
      };

      this.turnAnimationOff = function () {
        setTimeout(function(){
          $('.logo-part-animation-on').attr('class', 'logo-part-animation-off');
        }, 600);
      };

      this.triggerSpinLogo = function (ev, data) {
        this.trigger(document, events.ui.page.spinLogo);
      };

      this.triggerStopSpinningLogo = function(ev, data) {
        this.trigger(document, events.ui.page.stopSpinningLogo);
      };

      this.after('initialize', function () {
        this.on(document, events.ui.page.spinLogo, this.turnAnimationOn);
        this.on(document, events.ui.page.stopSpinningLogo, this.turnAnimationOff);

        this.on(document, events.ui.tag.select, this.triggerSpinLogo);
        this.on(document, events.mails.available, this.triggerStopSpinningLogo);
        this.on(document, events.mail.saveDraft, this.triggerSpinLogo);
        this.on(document, events.mail.draftSaved, this.triggerStopSpinningLogo);
        this.on(document, events.ui.mail.open, this.triggerSpinLogo);
        this.on(document, events.dispatchers.rightPane.openDraft, this.triggerSpinLogo);
        this.on(document, events.mail.want, this.triggerStopSpinningLogo);
      });
    }
  }
);
