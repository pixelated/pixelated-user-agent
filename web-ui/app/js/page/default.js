define(
  [
    'mail_view/ui/compose_box',
    'mail_list_actions/ui/mail_list_actions',
    'user_alerts/ui/user_alerts',
    'mail_list/ui/mail_list',
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
    'flight/lib/logger'
  ],

  function (
    composeBox,
    mailListActions,
    userAlerts,
    mailList,
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
    withLogging) {

    'use strict';
    function initialize(path) {
      viewI18n.init(path);
      paneContractExpand.attachTo(document);

      userAlerts.attachTo('#user-alerts');

      mailList.attachTo('#mail-list');
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
    }

    return initialize;
  }
);
