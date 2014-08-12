/*global _ */
/*global Pixelated */

define(
  [
    'flight/lib/component',
    'views/i18n',
    'services/model/mail',
    'page/events',
    'features'
  ], function (defineComponent, i18n, Mail, events, features) {

    'use strict';

    return defineComponent(mailService);

    function mailService() {
      var that;

      this.defaultAttrs({
        mailsResource: '/mails',
        singleMailResource: '/mail',
        currentTag: '',
        lastQuery: '',
        currentPage: 0,
        numPages: 0,
        w: 25
      });

      this.errorMessage = function(msg) {
        return function() {
          that.trigger(document, events.ui.userAlerts.displayMessage, { message: msg });
        };
      };

      this.updateTags = function(ev, data) {
        var that = this;
        var ident = data.ident;
        $.ajax('/mail/' + ident + '/tags', {
          type: 'POST',
          contentType: 'application/json; charset=utf-8',
          data: JSON.stringify({newtags: data.tags})
        }).done(function(data) {
          that.refreshResults();
          $(document).trigger(events.mail.tags.updated, { ident: ident, tags: data });
        })
        .fail(this.errorMessage(i18n('Could not update mail tags')));
      };

      this.readMail = function(ev, data) {
        var mailIdents;
        if (data.checkedMails) {
          mailIdents = _.map(data.checkedMails, function(mail) {
            return mail.ident;
          });
          $.ajax( '/mails/read', {
            type: 'POST',
            data: {idents: JSON.stringify(mailIdents)}
          }).done(this.triggerMailsRead(data.checkedMails));
        } else {
          $.ajax('/mail/' + data.ident + '/read', {type: 'POST'});
        }
      };

      this.unreadMail = function(ev, data) {
        var mailIdents;
        if (data.checkedMails) {
          mailIdents = _.map(data.checkedMails, function(mail) {
            return mail.ident;
          });
          $.ajax( '/mails/unread', {
            type: 'POST',
            data: {idents: JSON.stringify(mailIdents)}
          }).done(this.triggerMailsRead(data.checkedMails));
        } else {
          $.ajax('/mail/' + data.ident + '/read', {type: 'POST'});
        }
      };

      this.triggerMailsRead = function(mails) {
        return _.bind(function() {
          this.refreshResults();
          this.trigger(document, events.ui.mail.unchecked, { mails: mails });
          this.trigger(document, events.ui.mails.hasMailsChecked, false);
        }, this);
      };

      this.triggerDeleted = function(dataToDelete) {
        return _.bind(function() {
          var mails = dataToDelete.mails || [dataToDelete.mail];

          this.refreshResults();
          this.trigger(document, events.ui.userAlerts.displayMessage, { message: dataToDelete.successMessage});
          this.trigger(document, events.ui.mail.unchecked, { mails: mails });
          this.trigger(document, events.ui.mails.hasMailsChecked, false);
          this.trigger(document, events.mail.deleted, { mails: mails });
        }, this);
      };

      this.deleteMail = function(ev, data) {
        $.ajax('/mail/' + data.mail.ident,
               {type: 'DELETE'})
          .done(this.triggerDeleted(data))
          .fail(this.errorMessage(i18n('Could not delete email')));
      };

      this.deleteManyMails = function(ev, data) {
        var dataToDelete = data;
        var mailIdents = _.map(data.mails, function(mail) {
          return mail.ident;
        });

        $.ajax('/mails', {
          type: 'DELETE',
          data: {idents: JSON.stringify(mailIdents)}
        }).done(this.triggerDeleted(dataToDelete))
          .fail(this.errorMessage(i18n('Could not delete emails')));
      };

      function compileQuery(data) {
        var query = 'tag:"' + that.attr.currentTag + '"';

        if (data.tag === 'all') {
          query = 'in:all';
        }
        return query;
      }

      this.fetchByTag = function(ev, data) {
        this.attr.currentTag = data.tag;
        this.updateCurrentPageNumber(0);

        this.fetchMail(compileQuery(data), this.attr.currentTag, false, data);
      };

      this.refreshResults = function(ev, data) {
        var query = this.attr.lastQuery;
        this.fetchMail(query, this.attr.currentTag, true);
      };

      this.newSearch = function(ev, data) {
        var query = data.query;
        this.attr.currentTag = 'all';
        this.fetchMail(query, 'all');
      };

      this.mailFromJSON = function(mail) {
        return Mail.create(mail);
      };

      this.parseMails = function(data) {
        data.mails = _.map(data.mails, this.mailFromJSON, this);

        return data;
      };

      function escaped(s) {
        return encodeURI(s);
      }

      this.excludeTrashedEmailsForDraftsAndSent = function(query) {
        if (query === 'tag:"drafts"' || query === 'tag:"sent"') {
          return query + ' -in:"trash"';
        } else {
          return query;
        }
      };

      this.fetchMail = function(query, tag, fromRefresh, eventData) {
        var p = this.attr.currentPage;
        var w = this.attr.w;
        var url = this.attr.mailsResource + '?q='+ escaped(this.excludeTrashedEmailsForDraftsAndSent(query)) + '&p=' + p + '&w=' + w;
        this.attr.lastQuery = this.excludeTrashedEmailsForDraftsAndSent(query);
        $.ajax(url, { dataType: 'json' })
          .done(function(data) {
            this.attr.numPages = Math.ceil(data.stats.total / this.attr.w);
            var eventToTrigger = fromRefresh ? events.mails.availableForRefresh : events.mails.available;
            this.trigger(document, eventToTrigger, _.merge(_.merge({tag: tag }, eventData), this.parseMails(data)));
          }.bind(this))
          .fail(function() {
            this.trigger(document, events.ui.userAlerts.displayMessage, { message: i18n('Could not fetch messages') });
          }.bind(this));
      };

      function createSingleMailUrl(mailsResource, ident){
        return mailsResource + '/' + ident;
      }

      this.fetchSingle = function(event, data) {
        var fetchUrl = createSingleMailUrl(this.attr.singleMailResource, data.mail);

        $.ajax(fetchUrl, { dataType: 'json' })
          .done(function(mail) {
            if (_.isNull(mail)) {
              this.trigger(data.caller, events.mail.notFound);
              return;
            }

            this.trigger(data.caller, events.mail.here, { mail: this.mailFromJSON(mail) });
          }.bind(this));
      };

      this.previousPage = function() {
        if(this.attr.currentPage > 0) {
          this.updateCurrentPageNumber(this.attr.currentPage - 1);
          this.refreshResults();
        }
      };

      this.nextPage = function() {
        if(this.attr.currentPage < (this.attr.numPages - 1)) {
          this.updateCurrentPageNumber(this.attr.currentPage + 1);
          this.refreshResults();
        }
      };

      this.updateCurrentPageNumber = function(newCurrentPage) {
        this.attr.currentPage = newCurrentPage;
        this.trigger(document, events.ui.page.changed, {
          currentPage: this.attr.currentPage,
          numPages: this.attr.numPages
        });
      };

      this.wantDraftReplyForMail = function(ev, data) {
        $.ajax('/draft_reply_for/' + data.ident, { dataType: 'json' })
          .done(function(mail) {
            if (_.isNull(mail)) {
              this.trigger(document, events.mail.draftReply.notFound);
              return;
            }
            this.trigger(document, events.mail.draftReply.here, { mail: this.mailFromJSON(mail) });
          }.bind(this));
      };

      this.after('initialize', function () {
        that = this;

        this.on(events.mail.want, this.fetchSingle);
        this.on(events.mail.read, this.readMail);
        this.on(events.mail.unread, this.unreadMail);
        if(features.isEnabled('tags')) {
          this.on(events.mail.tags.update, this.updateTags);
        }
        this.on(events.mail.delete, this.deleteMail);
        this.on(events.mail.deleteMany, this.deleteManyMails);
        this.on(events.search.perform, this.newSearch);
        this.on(events.mail.draftReply.want, this.wantDraftReplyForMail);

        this.on(events.ui.mails.fetchByTag, this.fetchByTag);
        this.on(events.ui.mails.refresh, this.refreshResults);
        this.on(events.ui.page.previous, this.previousPage);
        this.on(events.ui.page.next, this.nextPage);
      });
    }
  }
);
