define(['mail_view/ui/recipients/recipients_iterator'], function (RecipientsIterator) {
  'use strict';

  function createRecipient() {
    return jasmine.createSpyObj('recipient', ['doSelect', 'doUnselect', 'destroy']);
  }

  var recipientsIterator,
    exitInput;

  function createIterator(elements) {
    return new RecipientsIterator({ elements: elements, exitInput: exitInput });
  }

  function resetMock(m) {
    m.destroy.calls.reset();m.doSelect.calls.reset();m.doUnselect.calls.reset();
  }

  beforeEach(function () {
    exitInput = $('<input>');
  });

  describe('moving left', function () {
    it('unselects the current element and selects the element in the left if there is one', function () {
      var elements = _.times(2, createRecipient);

      recipientsIterator = createIterator(elements);
      recipientsIterator.moveLeft();

      expect(elements[0].doSelect).toHaveBeenCalled();
      expect(elements[1].doUnselect).toHaveBeenCalled();
    });

    it('doesnt do anything if there are no elements in the left', function () {
      var elements = _.times(2, createRecipient);
      recipientsIterator = createIterator(elements);
      recipientsIterator.moveLeft();
      _.each(elements, resetMock);

      recipientsIterator.moveLeft();

      expect(elements[0].doSelect).not.toHaveBeenCalled();
      expect(elements[0].doUnselect).not.toHaveBeenCalled();
      expect(elements[1].doSelect).not.toHaveBeenCalled();
      expect(elements[1].doUnselect).not.toHaveBeenCalled();
    });

  });

  describe('moving right', function () {
    it('unselects the current element and selects the one in the right if there is one', function () {
      var elements = _.times(2, createRecipient);
      recipientsIterator = createIterator(elements);
      recipientsIterator.moveLeft();
      _.each(elements, resetMock);

      recipientsIterator.moveRight();

      expect(elements[0].doUnselect).toHaveBeenCalled();
      expect(elements[1].doSelect).toHaveBeenCalled();
    });

    it('unselects current element and focus on exit input if there are no elements on the right', function () {
      var elements = _.times(2, createRecipient);
      spyOn(exitInput, 'focus');

      recipientsIterator = createIterator(elements);
      recipientsIterator.moveRight();

      expect(elements[1].doUnselect).toHaveBeenCalled();
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
      expect(elements[0].doSelect).toHaveBeenCalled();
    });

    it('focus on the input if there are no more elements', function () {
      recipientsIterator = createIterator([createRecipient()]);
      spyOn(exitInput, 'focus');

      recipientsIterator.deleteCurrent();

      expect(exitInput.focus).toHaveBeenCalled();
    });
  });


});
