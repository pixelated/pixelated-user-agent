/*global Bloodhound */
define(
  ['page/events', 'features'],
  function (events, features) {
    function withMailTagging () {
      this.updateTags = function(mail, tags) {
        this.trigger(document, events.mail.tags.update, {ident: mail.ident, tags: tags});
      };

      this.attachTagCompletion = function() {
        if(!features.isEnabled('tags')) {
          return;
        }

        this.tagCompleter = new Bloodhound({
          datumTokenizer: function(d) { return [d.value]; },
          queryTokenizer: function(q) { return [q.trim()]; },
          remote: {
            url: '/tags?q=%QUERY',
            filter: function(pr) { return _.map(pr, function(pp) { return {value: pp.name}; }); }
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

      this.createNewTag = function() {
        if(features.isEnabled('createNewTag')) {
          var tagsCopy = this.attr.mail.tags.slice();
          tagsCopy.push(this.select('newTagInput').val());
          this.tagCompleter.clear();
          this.tagCompleter.clearPrefetchCache();
          this.tagCompleter.clearRemoteCache();
          this.updateTags(this.attr.mail, _.uniq(tagsCopy));
          this.trigger(document, events.dispatchers.tags.refreshTagList);
        }
      };

      this.after('displayMail', function () {
        this.on(this.select('newTagInput'), 'typeahead:selected typeahead:autocompleted', this.createNewTag);
      });
    };

    return withMailTagging;
  }
);
