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
'use strict';

define(
  [
    'helpers/view_helper',
    'views/templates',
    'page/events'
  ],
  function (viewHelper, templates, events) {

  function mailItem() {
    this.updateSelected = function (ev, data) {
      if (data.ident === this.attr.mail.ident) { this.doSelect(); }
      else { this.doUnselect(); }
    };

    this.isOpeningOnANewTab = function (ev) {
      return ev.metaKey || ev.ctrlKey || ev.which === 2;
    };

    this.doSelect = function () {
      this.$node.addClass('selected');
    };

    this.doUnselect = function () {
      this.$node.removeClass('selected');
    };

    this.doMailChecked = function (ev) {
      if (ev.target.checked) {
        this.checkCheckbox();
      } else {
        this.uncheckCheckbox();
      }
    };

    this.checkboxElement = function () {
      return this.$node.find('input[type=checkbox]');
    };

    this.checkCheckbox = function () {
      this.checkboxElement().prop('checked', true);
      this.trigger(document, events.ui.mail.checked, { mail: this.attr.mail});
    };

    this.uncheckCheckbox = function () {
      this.checkboxElement().prop('checked', false);
      this.trigger(document, events.ui.mail.unchecked, { mail: this.attr.mail});
    };

    this.render = function () {
      this.attr.mail.tagsForListView = _.without(this.attr.mail.tags, this.attr.tag);
      var mailItemHtml = templates.mails[this.attr.templateType](this.attr.mail);
      this.$node.html(mailItemHtml);
      this.$node.addClass(viewHelper.formatStatusClasses(this.attr.mail.status));
      if (this.attr.selected) { this.doSelect(); }
      this.on(this.$node.find('a'), 'click', this.triggerOpenMail);
    };

    this.after('initialize', function () {
      this.on(this.$node.find('input[type=checkbox]'), 'change', this.doMailChecked);
      this.on(document, events.ui.mails.cleanSelected, this.doUnselect);
      this.on(document, events.ui.tag.select, this.doUnselect);
      this.on(document, events.ui.tag.select, this.uncheckCheckbox);
      this.on(document, events.ui.mails.uncheckAll, this.uncheckCheckbox);
      this.on(document, events.ui.mails.checkAll, this.checkCheckbox);
    });
  }

  return mailItem;
});
