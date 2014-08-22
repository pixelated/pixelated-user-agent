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
define(function () {

  return Iterator;

  function Iterator(elems, startingIndex) {

    this.index = startingIndex || 0;
    this.elems = elems;

    this.hasPrevious = function () {
      return this.index != 0;
    };

    this.hasNext = function () {
      return this.index < this.elems.length - 1;
    };

    this.previous = function () {
      return this.elems[--this.index];
    };

    this.next = function () {
      return this.elems[++this.index];
    };

    this.current = function () {
      return this.elems[this.index];
    };

    this.hasElements = function () {
      return this.elems.length > 0;
    };

    this.removeCurrent = function () {
      var removed = this.current(),
        toRemove = this.index;

      !this.hasNext() && this.index--;
      this.elems.remove(toRemove);
      return removed;
    };
  }
});
