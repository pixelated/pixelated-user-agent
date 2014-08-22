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

define(
  [
    'flight/lib/component',
    'views/templates'
  ],

  function (defineComponent, templates) {

    return defineComponent(recipient);

    function recipient() {
      this.renderAndPrepend = function (nodeToPrependTo, recipient) {
        var html = $(templates.compose.fixedRecipient(recipient));
        html.insertBefore(nodeToPrependTo.children().last());
        var component = new this.constructor();
        component.initialize(html, recipient);
        return component;
      };

      this.destroy = function () {
        this.$node.remove();
        this.teardown();
      };

      this.select = function () {
        this.$node.find('.recipient-value').addClass('selected');
      };

      this.unselect = function () {
        this.$node.find('.recipient-value').removeClass('selected');
      };
    }
  }
);
