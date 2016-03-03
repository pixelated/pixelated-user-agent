describeComponent('search/results_highlighter', function () {
  'use strict';

  beforeEach(function () {
    this.setupComponent('<div id="text">Any one seeing too many open bugs</div>');
  });

  it('highlights words or parts of words that match with the keywords given', function () {
    this.component.attr = {keywords: ['any']};
    this.component.highlightResults(event, {where: '#text'});

    var highlightedWords = this.component.$node.find('.search-highlight').length;

    expect(highlightedWords).toEqual(2);
  });

  it('highlights a string with the keywords given', function () {
    this.component.attr = {keywords: ['foo']};
    var expectedString = 'the <em class="search-highlight">foo</em> bar';
    var string = this.component.highlightString('the foo bar');

    expect(string).toEqual(expectedString);
  });

  it('resets highlights when a new search is performed', function() {
    this.component.attr = {keywords: ['any']};
    this.component.highlightResults(event, {where: '#text'});
    $(document).trigger(Pixelated.events.search.resetHighlight);

    var highlightedWords = this.component.$node.find('.search-highlight').length;

    expect(highlightedWords).toEqual(0);
  });
});
