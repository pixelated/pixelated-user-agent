/*global _ */

define(
  [
    'flight/lib/component',
    'views/templates',
    'helpers/view_helper',
    'mail_list/ui/mail_items/mail_item',
    'page/events'
  ],

  function (defineComponent, templates, viewHelpers, mailItem, events) {
    'use strict';

    return defineComponent(draftItem, mailItem);

    function draftItem() {
      function isOpeningOnANewTab(ev) {
        return ev.metaKey || ev.ctrlKey || ev.which === 2;
      }

      this.triggerOpenMail = function (ev) {
        if (isOpeningOnANewTab(ev)) {
          return;
        }
        this.trigger(document, events.dispatchers.rightPane.openDraft, { ident: this.attr.ident });
        this.trigger(document, events.ui.mail.updateSelected, { ident: this.attr.ident });
        this.trigger(document, events.router.pushState, { mailIdent: this.attr.ident });
        ev.preventDefault(); // don't let the hashchange trigger a popstate
      };

      this.render = function () {
        var mailItemHtml = templates.mails.sent(this.attr);
        this.$node.html(mailItemHtml);
        this.$node.addClass(this.attr.statuses);
        if(this.attr.selected) { this.select(); }
        this.on(this.$node.find('a'), 'click', this.triggerOpenMail);
      };

      this.after('initialize', function () {
        this.initializeAttributes();
        this.render();
        this.attachListeners();

        if (this.attr.isChecked) {
          this.checkCheckbox();
        }

        this.on(document, events.ui.composeBox.newMessage, this.unselect);
        this.on(document, events.ui.mail.updateSelected, this.updateSelected);
        this.on(document, events.mails.teardown, this.teardown);
      });
    }
  }
);
