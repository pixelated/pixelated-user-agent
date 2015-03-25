describeComponent('search/results_highlighter', function () {
  'use strict';

  it('highlights only words that matches with the keywords given', function () {
    this.setupComponent('<div id="text">Any one seeing too many open bugs</div>');

    this.component.attr = {keywords: ["any"]};
    this.component.highlightResults(event, {where: '#text'});

    var highlightedWords = this.component.$node.find('.search-highlight').length;

    expect(highlightedWords).toEqual(1);
  });

});
