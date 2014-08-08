/*global _ */
/*global Pixelated */

define(
  [
    'flight/lib/component',
    'views/templates',
    'page/events'
  ], function (defineComponent, templates, events) {

    'use strict';

    return defineComponent(searchTrigger);

    function searchTrigger() {
      var placeHolder = 'Search results for: ';

      this.defaultAttrs({
        input: 'input[type=search]',
        form: 'form'
      });

      this.render = function() {
        this.$node.html(templates.search.trigger());
      };

      this.search = function(ev, data) {
        ev.preventDefault();
        var input = this.select('input');
        var value = input.val();
        input.blur();
        if(!_.isEmpty(value)){
          this.trigger(document, events.ui.tag.select, { tag: 'all', skipMailListRefresh: true });
          this.trigger(document, events.search.perform, { query: value });
        } else {
          this.trigger(document, events.ui.tag.select, { tag: 'all'});
          this.trigger(document, events.search.empty);
        }
      };

      this.clearInput = function(event, data) {
        if (!data.skipMailListRefresh)
          this.select('input').val('');
      };

      this.showOnlySearchTerms = function(event){
        var value = this.select('input').val();
        var searchTerms = value.slice(placeHolder.length);
        this.select('input').val(searchTerms);
      };

      this.showSearchTermsAndPlaceHolder = function(event){
        var value = this.select('input').val();
        if (value.length > 0){
          this.select('input').val(placeHolder + value);
        }
      };

      this.after('initialize', function () {
        this.render();
        this.on(this.select('form'), 'submit', this.search);
        this.on(this.select('input'), 'focus', this.showOnlySearchTerms);
        this.on(this.select('input'), 'blur', this.showSearchTermsAndPlaceHolder);
        this.on(document, events.ui.tag.selected, this.clearInput);
      });
    }
  }
);
