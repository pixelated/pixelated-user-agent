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

define(function() {
  'use strict';
  Handlebars.registerHelper('formatRecipients', function (header) {
    function wrapWith(begin, end) {
      return function (x) {
        return begin + Handlebars.Utils.escapeExpression(x) + end;
      };
    }

    var to = _.map(header.to, wrapWith('<span class="to">', '</span>'));
    var cc = _.map(header.cc, wrapWith('<span class="cc">cc: ', '</span>'));
    var bcc = _.map(header.bcc, wrapWith('<span class="bcc">bcc: ', '</span>'));

    return new Handlebars.SafeString(to.concat(cc, bcc).join(', '));
  });
});
