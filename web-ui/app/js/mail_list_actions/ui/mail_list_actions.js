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
    'views/templates',
    'page/events',
    'page/router/url_params',
    'mail_list_actions/ui/compose_trigger',
    'mail_list_actions/ui/refresh_trigger',
    'mail_list/domain/refresher',
    'mail_list_actions/ui/toggle_check_all_trigger',
    'mail_list_actions/ui/pagination_trigger',
    'mail_list_actions/ui/delete_many_trigger',
    'mail_list_actions/ui/recover_many_trigger',
    'mail_list_actions/ui/archive_many_trigger',
    'mail_list_actions/ui/mark_many_as_read_trigger',
    'mail_list_actions/ui/mark_as_unread_trigger'
  ],

  function (
    defineComponent,
    templates,
    events,
    urlParams,
    composeTrigger,
    refreshTrigger,
    refresher,
    toggleCheckAllMailTrigger,
    paginationTrigger,
    deleteManyTrigger,
    recoverManyTrigger,
    archiveManyTrigger,
    markManyAsReadTrigger,
    markAsUnreadTrigger
  ) {
    'use strict';
    return defineComponent(mailsActions);

    function mailsActions() {
      this.render = function() {
        this.$node.html(this.getActionsBoxTemplate());
        refreshTrigger.attachTo('#refresh-trigger');
        composeTrigger.attachTo('#compose-trigger');
        toggleCheckAllMailTrigger.attachTo('#toggle-check-all-emails');
        paginationTrigger.attachTo('#pagination-trigger');
        deleteManyTrigger.attachTo('#delete-selected');
        recoverManyTrigger.attachTo('#recover-selected');
        archiveManyTrigger.attachTo('#archive-selected');
        markManyAsReadTrigger.attachTo('#mark-selected-as-read');
        markAsUnreadTrigger.attachTo('#mark-selected-as-unread');
        refresher.attachTo(document);
      };

      this.getCurrentTag = function () {
        return this.attr.currentTag || urlParams.getTag();
      };

      this.updateCurrentTag = function (ev, data) {
        this.attr.currentTag = data.tag;
        this.render();
      };

      this.getActionsBoxTemplate = function () {
        if(this.getCurrentTag() === 'trash') {
          return templates.mailActions.trashActionsBox();
        } else {
          return templates.mailActions.actionsBox();
        }
      };

      this.after('initialize', function () {
        this.on(document, events.ui.tag.select, this.updateCurrentTag);
        this.render();
      });
    }
  }
);
