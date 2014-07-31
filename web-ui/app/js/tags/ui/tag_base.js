define(['views/i18n', 'page/events'], function(i18n, events) {

  function tagBase() {
    var ALWAYS_HIDE_BADGE_FOR = ['sent', 'trash', 'all'];
    var TOTAL_BADGE = ['drafts'];

    this.displayBadge = function(tag) {
      if(_.include(ALWAYS_HIDE_BADGE_FOR, tag.name)) { return false; }
      if(this.badgeType(tag) === 'total') {
        return tag.counts.total > 0;
      } else {
        return (tag.counts.total - tag.counts.read) > 0;
      }
    };

    this.badgeType = function(tag) {
      return _.include(TOTAL_BADGE, tag.name) ? 'total' : 'unread';
    };

  }

  return tagBase;

});
