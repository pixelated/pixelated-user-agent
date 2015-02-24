describeComponent('search/results_highlighter', function () {
  'use strict';
  var self;

  beforeEach(function () {
    self = this;
  });

  it('highlights only words that matches with the keywords given', function () {
    self.setupComponent('<div id="text">Any one seeing too many open bugs</div>');

    self.component.attr = {keywords: ["any"]};
    self.component.highlightResults(event, {where: '#text'});

    var highlightedWords = self.component.$node.find('.search-highlight').length;

    expect(highlightedWords).toEqual(1);
  });

});
