define(
  [
    'flight/lib/component',
    'page/router/url_params',
    'page/events'
  ],

  function(defineComponent, urlParams, events) {
    'use strict';

    return defineComponent(leftPaneDispatcher);

    function leftPaneDispatcher() {
      var initialized = false;

      this.refreshTagList = function () {
        this.trigger(document, events.tags.want, { caller: this.$node });
      };

      this.loadTags = function (ev, data) {
        this.trigger(document, events.ui.tagList.load, data);
      };

      this.selectTag = function (ev, data) {
        var tag = (data && data.tag) || urlParams.getTag();
        this.trigger(document, events.ui.tag.select, { tag: tag });
      };

      this.pushUrlState = function (ev, data) {
        if (initialized) {
          this.trigger(document, events.router.pushState, data);
        }
        initialized = true;

        if (data.skipMailListRefresh) {
          return;
        }

        this.trigger(document, events.ui.mails.fetchByTag, data);
      };

      this.after('initialize', function () {
        this.on(this.$node, events.tags.received, this.loadTags);
        this.on(document, events.dispatchers.tags.refreshTagList, this.refreshTagList);
        this.on(document, events.ui.tags.loaded, this.selectTag);
        this.on(document, events.ui.tag.selected, this.pushUrlState);
        this.trigger(document, events.tags.want, { caller: this.$node } );
      });
    }
  }
);
