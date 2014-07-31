'use strict';

define(
  ['helpers/view_helper',
  'page/events'], function (viewHelper, events) {

  function mailItem() {
    this.updateSelected = function (ev, data) {
      if(data.ident === this.attr.ident) { this.select(); }
      else { this.unselect(); }
    };

    this.formattedDate = function (date) {
      return viewHelper.getFormattedDate(new Date(date));
    };

    this.select = function () {
      this.$node.addClass('selected');
    };

    this.unselect = function () {
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

    this.initializeAttributes = function () {
      var mail = this.attr.mail;
      this.attr.ident = mail.ident;
      this.attr.header = mail.header;
      this.attr.ident = mail.ident;
      this.attr.statuses = viewHelper.formatStatusClasses(mail.status);
      this.attr.tags = mail.tags;
      this.attr.header.formattedDate = this.formattedDate(mail.header.date);
    };

    this.attachListeners = function () {
      this.on(this.$node.find('input[type=checkbox]'), 'change', this.triggerMailChecked);
      this.on(document, events.ui.mails.cleanSelected, this.unselect);
      this.on(document, events.ui.mails.uncheckAll, this.uncheckCheckbox);
      this.on(document, events.ui.mails.checkAll, this.checkCheckbox);
    };
  }

  return mailItem;
});
