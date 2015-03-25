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
            $(domIdent).highlightRegex(new RegExp('\\b' + keyword, 'i'), {
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
        this.on(document, events.search.resetHighlight, this.clearHighlights);

        this.on(document, events.search.highlightResults, this.highlightResults);
      });
    }
});
