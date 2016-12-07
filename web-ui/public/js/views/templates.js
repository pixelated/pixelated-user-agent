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

define(['hbs/templates'], function (templates) {
  'use strict';

  var Templates = {
    compose: {
      box: window.Pixelated['public/templates/compose/compose_box.hbs'],
      inlineBox: window.Pixelated['public/templates/compose/inline_box.hbs'],
      replySection: window.Pixelated['public/templates/compose/reply_section.hbs'],
      recipientInput: window.Pixelated['public/templates/compose/recipient_input.hbs'],
      fixedRecipient: window.Pixelated['public/templates/compose/fixed_recipient.hbs'],
      recipients: window.Pixelated['public/templates/compose/recipients.hbs'],
      feedback: window.Pixelated['public/templates/compose/feedback_box.hbs'],
      attachmentsList: window.Pixelated['public/templates/compose/attachments_list.hbs'],
      attachmentItem: window.Pixelated['public/templates/compose/attachment_item.hbs'],
      attachmentUploadItem: window.Pixelated['public/templates/compose/attachment_upload_item.hbs'],
      uploadAttachmentFailed: window.Pixelated['public/templates/compose/upload_attachment_failed.hbs']
    },
    tags: {
      tagList: window.Pixelated['public/templates/tags/tag_list.hbs'],
      tag: window.Pixelated['public/templates/tags/tag.hbs'],
      tagInner: window.Pixelated['public/templates/tags/tag_inner.hbs'],
      shortcut: window.Pixelated['public/templates/tags/shortcut.hbs']
    },
    userAlerts: {
      message: window.Pixelated['public/templates/user_alerts/message.hbs']
    },
    mails: {
      single: window.Pixelated['public/templates/mails/single.hbs'],
      fullView: window.Pixelated['public/templates/mails/full_view.hbs'],
      mailActions: window.Pixelated['public/templates/mails/mail_actions.hbs'],
      draft: window.Pixelated['public/templates/mails/draft.hbs'],
      sent: window.Pixelated['public/templates/mails/sent.hbs'],
      trash: window.Pixelated['public/templates/mails/trash.hbs']
    },
    mailActions: {
      actionsBox: window.Pixelated['public/templates/mail_actions/actions_box.hbs'],
      trashActionsBox: window.Pixelated['public/templates/mail_actions/trash_actions_box.hbs'],
      composeTrigger: window.Pixelated['public/templates/mail_actions/compose_trigger.hbs'],
      refreshTrigger: window.Pixelated['public/templates/mail_actions/refresh_trigger.hbs'],
      paginationTrigger: window.Pixelated['public/templates/mail_actions/pagination_trigger.hbs']
    },
    noMessageSelected: window.Pixelated['public/templates/compose/no_message_selected.hbs'],
    noMailsAvailable: window.Pixelated['public/templates/compose/no_mails_available.hbs'],
    search: {
      trigger: window.Pixelated['public/templates/search/search_trigger.hbs']
    },
    page: {
      userSettingsIcon: window.Pixelated['public/templates/page/user_settings_icon.hbs'],
      userSettingsBox: window.Pixelated['public/templates/page/user_settings_box.hbs'],
      logout: window.Pixelated['public/templates/page/logout.hbs'],
      logoutShortcut: window.Pixelated['public/templates/page/logout_shortcut.hbs'],
      version: window.Pixelated['public/templates/page/version.hbs']
    },
    feedback: {
      feedback: window.Pixelated['public/templates/feedback/feedback_trigger.hbs']
    }
  };

  Handlebars.registerPartial('tag_inner', Templates.tags.tagInner);
  Handlebars.registerPartial('recipients', Templates.compose.recipients);
  Handlebars.registerPartial('attachments_list', Templates.compose.attachmentsList);
  Handlebars.registerPartial('attachments_upload', Templates.compose.attachmentsList);
  Handlebars.registerPartial('attachment_item', Templates.compose.attachmentItem);
  Handlebars.registerPartial('attachment_upload_item', Templates.compose.attachmentUploadItem);
  Handlebars.registerPartial('uploadAttachmentFailed', Templates.compose.uploadAttachmentFailed);

  return Templates;
});
