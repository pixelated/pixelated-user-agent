define(
  [
    'flight/lib/component',
    'views/templates',
    'page/events'
  ],

  function(defineComponent, templates, events) {
    'use strict';

    return defineComponent(paginationTrigger);

    function paginationTrigger() {
      this.defaultAttrs({
        previous: '#left-arrow',
        next: '#right-arrow',
        currentPage: "#current-page"
      });

      this.renderWithPageNumber = function(pageNumber) {
        this.$node.html(templates.mailActions.paginationTrigger({
          currentPage: pageNumber
        }));
        this.on(this.attr.previous, 'click', this.previousPage);
        this.on(this.attr.next, 'click', this.nextPage);
      };

      this.render = function() {
        this.renderWithPageNumber(1);
      };

      this.updatePageDisplay = function(event, data) {
        this.renderWithPageNumber(data.currentPage + 1);
      };

      this.previousPage = function(event) {
        this.trigger(document, events.ui.page.previous);
      };

      this.nextPage = function(event) {
        this.trigger(document, events.ui.page.next);
      };

      this.after('initialize', function () {
        this.render();
        this.on(document, events.ui.page.changed, this.updatePageDisplay);
      });
    }
  }
);
