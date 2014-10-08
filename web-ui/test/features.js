define([], function() {
  'use strict';
  return {
    isEnabled: function(featureName) {
      return true;
    },
    isLogoutEnabled: function() {
      return true;
    },
    getLogoutUrl: function() {
      return '/test/logout/url';
    }
  };
});
