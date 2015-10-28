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
define(['helpers/iterator'], function (Iterator) {

  return RecipientsIterator;

  function RecipientsIterator(options) {

    this.iterator = new Iterator(options.elements, options.elements.length - 1);
    this.input = options.exitInput;

    this.current = function () {
      return this.iterator.current();
    };

    this.moveLeft = function () {
      if (this.iterator.hasPrevious()) {
        this.iterator.current().doUnselect();
        this.iterator.previous().doSelect();
      }
    };

    this.moveRight = function () {
      this.iterator.current().doUnselect();
      if (this.iterator.hasNext()) {
        this.iterator.next().doSelect();
      } else {
        this.input.focus();
      }
    };

    this.deleteCurrent = function () {
      this.iterator.removeCurrent().destroy();

      if (this.iterator.hasElements()) {
        this.iterator.current().doSelect();
      } else {
        this.input.focus();
      }
    };
  }

});
