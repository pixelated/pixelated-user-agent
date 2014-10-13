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
    'mail_view/data/mail_builder',
    'page/events',
    'features'
  ],
  function (defineComponent, mailBuilder, events, features) {
    'use strict';

    return defineComponent(mailSender);

    function mailSender() {
      function successSendMail(on){
        return function(result) {
          on.trigger(document, events.mail.sent, result);
        };
      }

      function successSaveDraft(on){
        return function(result){
          on.trigger(document, events.mail.draftSaved, result);
        };
      }

      function failure(on) {
        return function(xhr, status, error) {
          on.trigger(events.ui.userAlerts.displayMessage, {message: 'Ops! something went wrong, try again later.'});
        };
      }

      this.defaultAttrs({
        mailsResource: '/mails'
      });

      this.sendMail = function(event, data) {
        $.ajax(this.attr.mailsResource, {
          type: 'POST',
          dataType: 'json',
          contentType: 'application/json; charset=utf-8',
          data: JSON.stringify(data)
        }).done(successSendMail(this))
          .fail(failure(this));
      };

      this.saveMail = function(mail) {
        return $.ajax(this.attr.mailsResource, {
          type: 'PUT',
          dataType: 'json',
          contentType: 'application/json; charset=utf-8',
          data: JSON.stringify(mail)
        });
      };

      this.saveDraft = function(event, data) {
        this.saveMail(data)
          .done(successSaveDraft(this))
          .fail(failure(this));
      };

      this.saveMailWithCallback = function(event, data) {
        this.saveMail(data.mail)
          .done(function(result) { return data.callback(result); })
          .fail(function(result) { return data.callback(result); });
      };

      this.after('initialize', function () {
        this.on(events.mail.send, this.sendMail);
        if(features.isEnabled('saveDraft')) {
          this.on(events.mail.saveDraft, this.saveDraft);
        }
        this.on(document, events.mail.save, this.saveMailWithCallback);
      });
    }
  });
