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

'use strict';
define(
  ['page/events', 'features'],
  function (events, features) {
    function withMailTagging () {
      this.updateTags = function(mail, tags) {
        this.trigger(document, events.mail.tags.update, {ident: mail.ident, tags: tags});
      };

      this.attachTagCompletion = function(mail) {
        this.tagFilter = function (parsedResult) {
            var filtered = _.filter(parsedResult, function (tag) {return ! _.contains(mail.tags, tag.name); });
            return _.map(filtered, function(tag) { return {value: Handlebars.Utils.escapeExpression(tag.name)}; });
        };

        this.tagCompleter = new Bloodhound({
          datumTokenizer: function(d) { return [d.value]; },
          queryTokenizer: function(q) { return [q.trim()]; },
          remote: {
            url: '/tags?skipDefaultTags=true&q=%QUERY',
            filter: this.tagFilter
          }
        });

        this.tagCompleter.initialize();

        this.select('newTagInput').typeahead({
          hint: true,
          highlight: true,
          minLength: 1
        }, {
          source: this.tagCompleter.ttAdapter()
        });
      };

      this.createNewTag = function () {
        var tagsCopy = this.attr.mail.tags.slice();
        tagsCopy.push(this.select('newTagInput').val());
        this.tagCompleter.clear();
        this.tagCompleter.clearPrefetchCache();
        this.tagCompleter.clearRemoteCache();
        this.updateTags(this.attr.mail, _.uniq(tagsCopy));
      };

      this.after('displayMail', function () {
        this.on(this.select('newTagInput'), 'typeahead:selected typeahead:autocompleted', this.createNewTag);
      });
    }

    return withMailTagging;
  }
);
