/*global Handlebars */

define(['hbs/templates'], function (templates) {
  'use strict';

  var Templates = {
    compose: {
      box: window.Smail['app/templates/compose/compose_box.hbs'],
      inlineBox: window.Smail['app/templates/compose/inline_box.hbs'],
      replySection: window.Smail['app/templates/compose/reply_section.hbs'],
      recipientInput: window.Smail['app/templates/compose/recipient_input.hbs'],
      fixedRecipient: window.Smail['app/templates/compose/fixed_recipient.hbs'],
      recipients: window.Smail['app/templates/compose/recipients.hbs']
    },
    tags: {
      tagList: window.Smail['app/templates/tags/tag_list.hbs'],
      tag: window.Smail['app/templates/tags/tag.hbs'],
      tagInner: window.Smail['app/templates/tags/tag_inner.hbs'],
      shortcut: window.Smail['app/templates/tags/shortcut.hbs']
    },
    userAlerts: {
      message: window.Smail['app/templates/user_alerts/message.hbs']
    },
    mails: {
      single: window.Smail['app/templates/mails/single.hbs'],
      fullView: window.Smail['app/templates/mails/full_view.hbs'],
      mailActions: window.Smail['app/templates/mails/mail_actions.hbs'],
      sent: window.Smail['app/templates/mails/sent.hbs']
    },
    mailActions: {
      actionsBox: window.Smail['app/templates/mail_actions/actions_box.hbs'],
      composeTrigger: window.Smail['app/templates/mail_actions/compose_trigger.hbs'],
      refreshTrigger: window.Smail['app/templates/mail_actions/refresh_trigger.hbs'],
      paginationTrigger: window.Smail['app/templates/mail_actions/pagination_trigger.hbs']
    },
    noMessageSelected: window.Smail['app/templates/no_message_selected.hbs'],
    search: {
      trigger: window.Smail['app/templates/search/search_trigger.hbs']
    }
  };

  Handlebars.registerPartial('tag_inner', Templates.tags.tagInner);
  Handlebars.registerPartial('recipients', Templates.compose.recipients);

  return Templates;
});
