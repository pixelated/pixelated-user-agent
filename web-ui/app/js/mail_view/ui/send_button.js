/*global _ */
'use strict';

define([
    'flight/lib/component',
    'flight/lib/utils',
    'page/events'
  ],
  function (defineComponent, utils, events) {

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

        this.trigger(document, events.ui.recipients.doCompleteInput);
      };

      this.after('initialize', function () {
        this.attr.recipients = {};
        this.attr.inputHasMail = {};

        this.on(document, events.ui.recipients.inputHasMail, this.inputHasMail);
        this.on(document, events.ui.recipients.inputHasNoMail, this.inputHasNoMail);
        this.on(document, events.ui.recipients.updated, this.updateRecipientsForField);

        this.on(this.$node, 'click', this.updateRecipientsAndSendMail);

        this.on(document, events.dispatchers.rightPane.clear, this.teardown);
        this.on(document, events.ui.sendbutton.enable, this.enableButton);

        this.disableButton();
      });
    }

  }
);
