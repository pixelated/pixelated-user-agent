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
    'mail_list/ui/mail_items/mail_item',
    'page/events'
  ],

  function (defineComponent, mailItem, events) {
    'use strict';

    return defineComponent(sentItem, mailItem);

    function sentItem() {
      this.triggerOpenMail = function (ev) {
        if (this.isOpeningOnANewTab(ev)) {
          return;
        }
        this.trigger(document, events.ui.mail.open, { ident: this.attr.ident });
        this.trigger(document, events.router.pushState, { mailIdent: this.attr.ident });
        ev.preventDefault(); // don't let the hashchange trigger a popstate
      };

      this.openMail = function (ev, data) {
        if (data.ident !== this.attr.ident) {
          return;
        }
        this.trigger(document, events.ui.mail.updateSelected, { ident: this.attr.ident });
      };

      this.after('initialize', function () {
        this.initializeAttributes();
        this.attr.tagsForListView = _.without(this.attr.tags, this.attr.tag);
        this.render();
        this.attachListeners();

        if (this.attr.isChecked) {
          this.checkCheckbox();
        }

        this.on(document, events.ui.composeBox.newMessage, this.doUnselect);
        this.on(document, events.ui.mail.open, this.openMail);
        this.on(document, events.ui.mail.updateSelected, this.updateSelected);
        this.on(document, events.mails.teardown, this.teardown);
      });
    }
  }
);
