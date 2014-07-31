'use strict';

define(
  [
    'flight/lib/component',
    'views/templates',
    'mail_list_actions/ui/compose_trigger',
    'mail_list_actions/ui/refresh_trigger',
    'mail_list/domain/refresher',
    'mail_list_actions/ui/toggle_check_all_trigger',
    'mail_list_actions/ui/pagination_trigger',
    'mail_list_actions/ui/delete_many_trigger',
    'mail_list_actions/ui/mark_many_as_read_trigger',
    'mail_list_actions/ui/mark_as_unread_trigger'
  ],

  function (
    defineComponent,
    templates,
    composeTrigger,
    refreshTrigger,
    refresher,
    toggleCheckAllMailTrigger,
    paginationTrigger,
    deleteManyTrigger,
    markManyAsReadTrigger,
    markAsUnreadTrigger
  ) {

    return defineComponent(mailsActions);

    function mailsActions() {
      this.render = function() {
        this.$node.html(templates.mailActions.actionsBox);
        refreshTrigger.attachTo('#refresh-trigger');
        composeTrigger.attachTo('#compose-trigger');
        toggleCheckAllMailTrigger.attachTo('#toggle-check-all-emails');
        paginationTrigger.attachTo('#pagination-trigger');
        deleteManyTrigger.attachTo('#delete-selected');
        markManyAsReadTrigger.attachTo('#mark-selected-as-read');
        markAsUnreadTrigger.attachTo('#mark-selected-as-unread');
        refresher.attachTo(document);
      };

      this.after('initialize', function () {
        this.render();
      });
    }
  }
);
