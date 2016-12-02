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
    'page/events',
    'views/i18n'
  ],

  function (defineComponent, events, i18n) {
    'use strict';

    return defineComponent(draftSaveStatus);

    function draftSaveStatus() {
      this.setMessage = function(msg) {
        var node = this.$node;
        return function () { node.text(msg); };
      };

      this.after('initialize', function () {
        this.on(document, events.mail.saveDraft, this.setMessage(i18n.t('draft-saving')));
        this.on(document, events.mail.draftSaved, this.setMessage(i18n.t('draft-saved')));
        this.on(document, events.ui.mail.changedSinceLastSave, this.setMessage(''));
      });
    }
  }
);
