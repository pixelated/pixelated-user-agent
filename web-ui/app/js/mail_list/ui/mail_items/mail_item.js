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
      if(data.ident === this.attr.ident) { this.doSelect(); }
      else { this.doUnselect(); }
    };

    this.formattedDate = function (date) {
      return viewHelper.getFormattedDate(new Date(date));
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

    this.triggerMailChecked = function (ev, data) {
      var eventToTrigger = ev.target.checked ? events.ui.mail.checked : events.ui.mail.unchecked;
      this.trigger(document, eventToTrigger, { mail: this.attr.mail});
    };

    this.checkboxElement = function () {
      return this.$node.find('input[type=checkbox]');
    };

    this.checkCheckbox = function () {
      this.checkboxElement().prop('checked', true);
      this.triggerMailChecked({'target': {'checked': true}});
    };

    this.uncheckCheckbox = function () {
      this.checkboxElement().prop('checked', false);
      this.triggerMailChecked({'target': {'checked': false}});
    };

    this.render = function () {
      this.attr.tagsForListView = _.without(this.attr.tags, this.attr.tag);
      var mailItemHtml = templates.mails[this.attr.templateType](this.attr);
      this.$node.html(mailItemHtml);
      this.$node.addClass(this.attr.statuses);
      if(this.attr.selected) { this.doSelect(); }
      this.on(this.$node.find('a'), 'click', this.triggerOpenMail);
    };

    this.initializeAttributes = function () {
      var mail = this.attr.mail;
      this.attr.ident = mail.ident;
      this.attr.header = mail.header;
      this.attr.ident = mail.ident;
      this.attr.statuses = viewHelper.formatStatusClasses(mail.status);
      this.attr.tags = mail.tags;
      this.attr.attachments = mail.attachments;
      this.attr.mailbox = mail.mailbox;
      this.attr.header.formattedDate = this.formattedDate(mail.header.date);
    };

    this.attachListeners = function () {
      this.on(this.$node.find('input[type=checkbox]'), 'change', this.triggerMailChecked);
      this.on(document, events.ui.mails.cleanSelected, this.doUnselect);
      this.on(document, events.ui.tag.select, this.doUnselect);
      this.on(document, events.ui.mails.uncheckAll, this.uncheckCheckbox);
      this.on(document, events.ui.mails.checkAll, this.checkCheckbox);
    };
  }

  return mailItem;
});
