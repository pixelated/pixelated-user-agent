/*global Smail */
/*global _ */

define(
  [
    'flight/lib/component',
    'page/events'
  ], function (defineComponent, events) {

    'use strict';

    return defineComponent(resultsHighlighter);

    function resultsHighlighter(){
      this.defaultAttrs({
        keywords: []
      });

      this.getKeywordsSearch = function (event, data) {
        this.attr.keywords = data.query.split(' ').map(function(keyword) {
          return keyword.toLowerCase();
        });
      };

      this.highlightResults = function (event, data) {
        var domIdent = data.where;
        if(this.attr.keywords) {
          _.each(this.attr.keywords, function (keyword) {
            $(domIdent).highlightRegex(new RegExp(keyword, 'i'), {
              tagType:   'em',
              className: 'search-highlight'
            });
          });
        }
      };

      this.clearHighlights = function (event, data) {
        this.attr.keywords = [];
        _.each($('em.search-highlight'), function(highlighted) {
          var jqueryHighlighted = $(highlighted);
          var text = jqueryHighlighted.text();
          jqueryHighlighted.replaceWith(text);
        });
      };

      this.after('initialize', function () {
        this.on(document, events.search.perform, this.getKeywordsSearch);
        this.on(document, events.ui.tag.select, this.clearHighlights);

        this.on(document, events.search.highlightResults, this.highlightResults);
      });
    }
});
