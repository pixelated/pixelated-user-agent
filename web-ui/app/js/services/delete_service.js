/*global _ */

define(['flight/lib/component', 'page/events', 'views/i18n'], function (defineComponent, events, i18n) {
  'use strict';

  return defineComponent(function() {

    this.successDeleteMessageFor = function(mail) {
      return mail.isInTrash() ?
        i18n('Your message was permanently deleted!') :
        i18n('Your message was moved to trash!');
    };

    this.successDeleteManyMessageFor = function(mail) {
      return mail.isInTrash() ?
        i18n('Your messages were permanently deleted!') :
        i18n('Your messages were moved to trash!');
    };

    this.deleteEmail = function (event, data) {
      this.trigger(document, events.mail.delete, {
        mail: data.mail,
        successMessage: this.successDeleteMessageFor(data.mail)
      });
    };

    this.deleteManyEmails = function (event, data) {
      var emails = _.values(data.checkedMails),
         firstEmail = emails[_.first(_.keys(emails))];

      this.trigger(document, events.mail.deleteMany, {
        mails: emails,
        successMessage: this.successDeleteManyMessageFor(firstEmail)
      });
    };

    this.after('initialize', function () {
      this.on(document, events.ui.mail.delete, this.deleteEmail);
      this.on(document, events.ui.mail.deleteMany, this.deleteManyEmails);
    });

  });
});
