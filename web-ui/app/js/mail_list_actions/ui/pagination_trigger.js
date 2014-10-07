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
    'page/events'
  ],

  function(defineComponent, templates, events) {
    'use strict';

    return defineComponent(paginationTrigger);

    function paginationTrigger() {
      this.defaultAttrs({
        previous: '#left-arrow',
        next: '#right-arrow',
        currentPage: '#current-page'
      });

      this.renderWithPageNumber = function(pageNumber) {
        this.$node.html(templates.mailActions.paginationTrigger({
          currentPage: pageNumber
        }));
        this.on(this.attr.previous, 'click', this.previousPage);
        this.on(this.attr.next, 'click', this.nextPage);
      };

      this.render = function() {
        this.renderWithPageNumber(1);
      };

      this.updatePageDisplay = function(event, data) {
        this.renderWithPageNumber(data.currentPage + 1);
      };

      this.previousPage = function(event) {
        this.trigger(document, events.ui.page.previous);
      };

      this.nextPage = function(event) {
        this.trigger(document, events.ui.page.next);
      };

      this.after('initialize', function () {
        this.render();
        this.on(document, events.ui.page.changed, this.updatePageDisplay);
      });
    }
  }
);
