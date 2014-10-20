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
/*global _ */

define(
  [
    'flight/lib/component',
    'flight/lib/utils',
    'mail_list/ui/mail_item_factory',
    'page/router/url_params',
    'page/events'
  ],

  function (defineComponent, utils, MailItemFactory, urlParams, events) {
    'use strict';

    return defineComponent(mailList);

    function mailList() {
      var self;

      var openMailEventFor = function (tag) {
        return tag === 'drafts' ? events.dispatchers.rightPane.openDraft : events.ui.mail.open;
      };

      this.defaultAttrs({
        mail: '.mail',
        currentMailIdent: '',
        urlParams: urlParams,
        initialized: false,
        checkedMails: {}
      });

      function appendMail(mail) {
        var isChecked = mail.ident in self.attr.checkedMails;
        MailItemFactory.createAndAttach(self.$node, mail, self.attr.currentMailIdent, self.attr.currentTag, isChecked);
      }

      function resetMailList() {
        self.trigger(document, events.mails.teardown);
        self.$node.empty();
      }

      function triggerMailOpenForPopState(data) {
        if(data.mailIdent) {
          self.trigger(document, openMailEventFor(data.tag), { ident: data.mailIdent });
        }
      }

      function shouldSelectEmailFromUrlMailIdent() {
        return self.attr.urlParams.hasMailIdent();
      }

      function selectMailBasedOnUrlMailIdent() {
        var mailIdent = self.attr.urlParams.getMailIdent();
        self.trigger(document, openMailEventFor(self.attr.currentTag), { ident: mailIdent });
        self.trigger(document, events.router.pushState, { tag: self.attr.currentTag, mailIdent: mailIdent });
      }

      function updateCurrentTagAndMail(data) {
        if (data.ident) {
          self.attr.currentMailIdent = data.ident;
        }

        self.attr.currentTag = data.tag || self.attr.currentTag;

	  self.updateCheckAllCheckbox();
      }

      function renderMails(mails) {
        _.each(mails, appendMail);
        self.trigger(document, events.search.highlightResults, {where: '#mail-list'});
        self.trigger(document, events.search.highlightResults, {where: '.bodyArea'});
        self.trigger(document, events.search.highlightResults, {where: '.subjectArea'});
        self.trigger(document, events.search.highlightResults, {where: '.msg-header .recipients'});

      }

      this.triggerScrollReset = function() {
        this.trigger(document, events.dispatchers.middlePane.resetScroll);
      };

      this.showMails = function (event, data) {
        updateCurrentTagAndMail(data);
        this.refreshMailList(null, data);
        this.triggerScrollReset();
        triggerMailOpenForPopState(data);
        this.openMailFromUrl();
      };

      this.refreshMailList = function (ev, data) {
        if (ev) { // triggered by the event, so we need to refresh the tag list
          this.trigger(document, events.dispatchers.tags.refreshTagList, { skipMailListRefresh: true });
        }
        resetMailList();
        renderMails(data.mails);
      };

      this.updateSelected = function (ev, data) {
        if(data.ident !== this.attr.currentMailIdent){
          this.uncheckCurrentMail();
          this.attr.currentMailIdent = data.ident;
        }
        this.checkCurrentMail();
      };

      this.checkCurrentMail = function() {
        $('#mail-'+this.attr.currentMailIdent+' input:checkbox')
          .attr('checked', true)
          .trigger('change');
      };

      this.uncheckCurrentMail = function() {
        $('#mail-'+this.attr.currentMailIdent+' input:checkbox')
          .attr('checked', false)
          .trigger('change');
      };

      this.cleanSelected = function () {
        this.attr.currentMailIdent = '';
      };

      this.respondWithCheckedMails = function (ev, caller) {
        this.trigger(caller, events.ui.mail.hereChecked, { checkedMails : this.checkedMailsForCurrentTag()});
      };

      this.updateCheckAllCheckbox = function () {
        if (this.checkedMailsForCurrentTag().length > 0) {
          this.trigger(document, events.ui.mails.hasMailsChecked, true);
        } else {
          this.trigger(document, events.ui.mails.hasMailsChecked, false);
        }
      };

	this.checkedMailsForCurrentTag = function() {
	    var checkedMailsForCurrentTag =  _.filter(self.attr.checkedMails, function(mail) {
		  return _.contains(mail.tags, self.attr.currentTag);
	    });
	    
	    return checkedMailsForCurrentTag.length > 0 ? checkedMailsForCurrentTag : {};
	}

      this.addToSelectedMails = function (ev, data) {
        this.attr.checkedMails[data.mail.ident] = data.mail;
        this.updateCheckAllCheckbox();
      };

      this.removeFromSelectedMails = function (ev, data) {
        if (data.mails) {
          _.each(data.mails, function(mail) {
            delete this.attr.checkedMails[mail.ident];
          }, this);
        } else {
          delete this.attr.checkedMails[data.mail.ident];
        }
        this.updateCheckAllCheckbox();
      };

      this.refreshWithScroll = function () {
        this.trigger(document, events.ui.mails.refresh);
        this.triggerScrollReset();
      };

      this.refreshAfterSaveDraft = function () {
        if(this.attr.currentTag === 'drafts') {
          this.refreshWithScroll();
        }
      };

      this.refreshAfterMailSent = function () {
        if(this.attr.currentTag === 'drafts' || this.attr.currentTag === 'sent') {
          this.refreshWithScroll();
        }
      };

      this.after('initialize', function () {
        self = this;

        this.on(document, events.ui.mails.cleanSelected, this.cleanSelected);

        this.on(document, events.mails.available, this.showMails);
        this.on(document, events.mails.availableForRefresh, this.refreshMailList);

        this.on(document, events.mail.draftSaved, this.refreshAfterSaveDraft);
        this.on(document, events.mail.sent, this.refreshAfterMailSent);

        this.on(document, events.ui.mail.updateSelected, this.updateSelected);
        this.on(document, events.ui.mail.wantChecked, this.respondWithCheckedMails);
        this.on(document, events.ui.mail.checked, this.addToSelectedMails);
        this.on(document, events.ui.mail.unchecked, this.removeFromSelectedMails);

        this.openMailFromUrl = utils.once(function () {
          if(shouldSelectEmailFromUrlMailIdent()) {
            selectMailBasedOnUrlMailIdent();
          }
        });

      });
    }
  }
);
