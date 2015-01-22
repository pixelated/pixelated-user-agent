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
    'mail_view/ui/compose_box',
    'mail_list_actions/ui/mail_list_actions',
    'user_alerts/ui/user_alerts',
    'mail_list/ui/mail_list',
    'mail_list/ui/mail_syncing_progress_bar',
    'mail_view/ui/no_message_selected_pane',
    'mail_view/ui/mail_view',
    'mail_view/ui/mail_actions',
    'mail_view/ui/reply_section',
    'mail_view/data/mail_sender',
    'services/mail_service',
    'services/delete_service',
    'tags/ui/tag_list',
    'tags/data/tags',
    'page/router',
    'dispatchers/right_pane_dispatcher',
    'dispatchers/middle_pane_dispatcher',
    'dispatchers/left_pane_dispatcher',
    'search/search_trigger',
    'search/results_highlighter',
    'foundation/off_canvas',
    'page/pane_contract_expand',
    'views/i18n',
    'views/recipientListFormatter',
    'flight/lib/logger',
    'page/logout'
  ],

  function (
    composeBox,
    mailListActions,
    userAlerts,
    mailList,
    mailSyncingProgressBar,
    noMessageSelectedPane,
    mailView,
    mailViewActions,
    replyButton,
    mailSender,
    mailService,
    deleteService,
    tagList,
    tags,
    router,
    rightPaneDispatcher,
    middlePaneDispatcher,
    leftPaneDispatcher,
    searchTrigger,
    resultsHighlighter,
    offCanvas,
    paneContractExpand,
    viewI18n,
    recipientListFormatter,
    withLogging,
    logout) {

    'use strict';
    function initialize(path) {
      viewI18n.init(path + '/assets/');
      paneContractExpand.attachTo(document);

      userAlerts.attachTo('#user-alerts');

      mailList.attachTo('#mail-list');
      mailSyncingProgressBar.attachTo('#mail-syncing-progress-bar');
      mailListActions.attachTo('#list-actions');

      searchTrigger.attachTo('#search-trigger');
      resultsHighlighter.attachTo(document);

      mailSender.attachTo(document);

      mailService.attachTo(document);
      deleteService.attachTo(document);

      tags.attachTo(document);
      tagList.attachTo('#tag-list');

      router.attachTo(document);

      rightPaneDispatcher.attachTo(document);
      middlePaneDispatcher.attachTo(document);
      leftPaneDispatcher.attachTo(document);

      offCanvas.attachTo(document);
      logout.attachTo('#logout');
    }

    return initialize;
  }
);
