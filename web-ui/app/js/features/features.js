define([], function() {
  var cachedDisabledFeatures;

  function getFeatures() {
    cachedDisabledFeatures = cachedDisabledFeatures || fetchDisabledFeatures();
    return cachedDisabledFeatures;
  }

  function fetchDisabledFeatures() {
    var disabledFeatures;
    $.ajax('/disabled_features', {
      async: false,
      success: function (results){
        disabledFeatures = results;
      },
      error: function () {
        console.error('Could not load feature toggles');
      }
    });
    return disabledFeatures;
  }

  return {
    isEnabled: function(featureName) {
      return ! _.contains(getFeatures(), featureName);
    }
  };
});
