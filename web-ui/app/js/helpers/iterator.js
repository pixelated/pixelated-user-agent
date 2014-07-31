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