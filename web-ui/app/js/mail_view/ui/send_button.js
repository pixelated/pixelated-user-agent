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

define([
    'flight/lib/component',
    'flight/lib/utils',
    'page/events',
    'helpers/view_helper'
  ],
  function (defineComponent, utils, events, viewHelper) {

    return defineComponent(sendButton);

    function sendButton() {
      var RECIPIENTS_BOXES_COUNT = 3;

      this.enableButton = function () {
        this.$node.prop('disabled', false);
      };

      this.disableButton = function () {
        this.$node.prop('disabled', true);
      };

      this.atLeastOneFieldHasRecipients = function () {
        return _.any(_.values(this.attr.recipients), function (e) { return !_.isEmpty(e); });
      };

      this.atLeastOneInputHasMail = function () {
        return _.any(_.values(this.attr.inputHasMail), function (e) { return e === true; });
      };

      this.updateButton = function () {
        if (this.atLeastOneInputHasMail() || this.atLeastOneFieldHasRecipients()) {
          this.enableButton();
        } else {
          this.disableButton();
        }
      };

      this.inputHasNoMail = function (ev, data) {
        this.attr.inputHasMail[data.name] = false;
        this.updateButton();
      };

      this.inputHasMail = function (ev, data) {
        this.attr.inputHasMail[data.name] = true;
        this.updateButton();
      };

      this.updateRecipientsForField = function (ev, data) {
        this.attr.recipients[data.recipientsName] = data.newRecipients;
        this.attr.inputHasMail[data.recipientsName] = false;

        this.updateButton();
      };

      this.updateRecipientsAndSendMail = function () {

        this.on(document, events.ui.mail.recipientsUpdated, utils.countThen(RECIPIENTS_BOXES_COUNT, function () {
          this.trigger(document, events.ui.mail.send);
          this.off(document, events.ui.mail.recipientsUpdated);
        }.bind(this)));

        this.disableButton();
        this.$node.text(viewHelper.i18n('sending-mail'));

        this.trigger(document, events.ui.recipients.doCompleteInput);
      };

      this.forceEnableButton = function () {
        this.enableButton();
        this.$node.html(viewHelper.i18n('send-button'));
      };

      this.after('initialize', function () {
        this.attr.recipients = {};
        this.attr.inputHasMail = {};
        this.$node.html(viewHelper.i18n('send-button'));

        this.on(document, events.ui.recipients.inputHasMail, this.inputHasMail);
        this.on(document, events.ui.recipients.inputHasNoMail, this.inputHasNoMail);
        this.on(document, events.ui.recipients.updated, this.updateRecipientsForField);

        this.on(this.$node, 'click', this.updateRecipientsAndSendMail);

        this.on(document, events.dispatchers.rightPane.clear, this.teardown);
        this.on(document, events.ui.sendbutton.enable, this.enableButton);
        this.on(document, events.mail.send_failed, this.forceEnableButton);

        this.disableButton();
      });
    }

  }
);
