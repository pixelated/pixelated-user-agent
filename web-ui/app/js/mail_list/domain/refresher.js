define(['flight/lib/component', 'page/events'], function(defineComponent, events) {
    'use strict';

    return defineComponent(refresher);

    function refresher() {
      this.defaultAttrs({
        interval: 20000
      });

      this.setupRefresher = function() {
        setTimeout(this.doRefresh.bind(this), this.attr.interval);
      };

      this.doRefresh = function() {
        this.trigger(document, events.ui.mails.refresh);
        this.setupRefresher();
      };

      this.after('initialize', function () {
        this.setupRefresher();
      });
    }
  }
);
