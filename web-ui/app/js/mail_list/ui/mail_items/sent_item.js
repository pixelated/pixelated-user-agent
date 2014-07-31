/*global _ */

define(
  [
    'flight/lib/component',
    'views/templates',
    'mail_list/ui/mail_items/mail_item',
    'page/events'
  ],

  function (defineComponent, templates, mailItem, events) {
    'use strict';

    return defineComponent(sentItem, mailItem);

    function sentItem() {
      function isOpeningOnANewTab(ev) {
        return ev.metaKey || ev.ctrlKey || ev.which == 2;
      }

      this.triggerOpenMail = function (ev) {
        if (isOpeningOnANewTab(ev)) {
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

      this.render = function () {
        this.attr.tagsForListView = _.without(this.attr.tags, this.attr.tag);
        var mailItemHtml = templates.mails.sent(this.attr);
        this.$node.html(mailItemHtml);
        this.$node.addClass(this.attr.statuses);
        this.attr.selected && this.select();
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
        this.on(document, events.ui.mail.open, this.openMail);
        this.on(document, events.ui.mail.updateSelected, this.updateSelected);
        this.on(document, events.mails.teardown, this.teardown);
      });
    }
  }
);
