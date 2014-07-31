/* global Smail */

define(['mail_view/ui/recipients/recipients_iterator'], function (RecipientsIterator) {
  'use strict';

  function createRecipient() {
    return jasmine.createSpyObj('recipient', ['select', 'unselect', 'destroy']);
  }

  var recipientsIterator,
    exitInput;

  function createIterator(elements) {
    return recipientsIterator = new RecipientsIterator({ elements: elements, exitInput: exitInput });
  }

  function resetMock(m) {
    m.destroy.reset();m.select.reset();m.unselect.reset();
  }

  beforeEach(function () {
    exitInput = $('<input>');
  });

  describe('moving left', function () {
    it('unselects the current element and selects the element in the left if there is one', function () {
      var elements = _.times(2, createRecipient);

      recipientsIterator = createIterator(elements);
      recipientsIterator.moveLeft();

      expect(elements[0].select).toHaveBeenCalled();
      expect(elements[1].unselect).toHaveBeenCalled();
    });

    it('doesnt do anything if there are no elements in the left', function () {
      var elements = _.times(2, createRecipient);
      recipientsIterator = createIterator(elements);
      recipientsIterator.moveLeft();
      _.each(elements, resetMock);

      recipientsIterator.moveLeft();

      expect(elements[0].select).not.toHaveBeenCalled();
      expect(elements[0].unselect).not.toHaveBeenCalled();
      expect(elements[1].select).not.toHaveBeenCalled();
      expect(elements[1].unselect).not.toHaveBeenCalled();
    });

  });

  describe('moving right', function () {
    it('unselects the current element and selects the one in the right if there is one', function () {
      var elements = _.times(2, createRecipient);
      recipientsIterator = createIterator(elements);
      recipientsIterator.moveLeft();
      _.each(elements, resetMock);

      recipientsIterator.moveRight();

      expect(elements[0].unselect).toHaveBeenCalled();
      expect(elements[1].select).toHaveBeenCalled();
    });

    it('unselects current element and focus on exit input if there are no elements on the right', function () {
      var elements = _.times(2, createRecipient);
      spyOn(exitInput, 'focus');

      recipientsIterator = createIterator(elements);
      recipientsIterator.moveRight();

      expect(elements[1].unselect).toHaveBeenCalled();
      expect(exitInput.focus).toHaveBeenCalled();
    });
  });

  describe('delete current', function () {
    it('selects what is left in the right after deleting the current element', function () {
      var elements = _.times(2, createRecipient);
      var toBeDeleted = elements[0];
      recipientsIterator = createIterator(elements);
      recipientsIterator.moveLeft();

      recipientsIterator.deleteCurrent();

      expect(toBeDeleted.destroy).toHaveBeenCalled();
      expect(elements[0].select).toHaveBeenCalled();
    });

    it('focus on the input if there are no more elements', function () {
      recipientsIterator = createIterator([createRecipient()]);
      spyOn(exitInput, 'focus');

      recipientsIterator.deleteCurrent();

      expect(exitInput.focus).toHaveBeenCalled();
    });
  });


});