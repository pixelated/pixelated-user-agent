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
        this.iterator.current().unselect();
        this.iterator.previous().select();
      }
    };

    this.moveRight = function () {
      this.iterator.current().unselect();
      if (this.iterator.hasNext()) {
        this.iterator.next().select();
      } else {
        this.input.focus();
      }
    };

    this.deleteCurrent = function () {
      this.iterator.removeCurrent().destroy();

      if (this.iterator.hasElements()) {
        this.iterator.current().select()
      } else {
        this.input.focus();
      }
    };
  }

});