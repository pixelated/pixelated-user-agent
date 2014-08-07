define([], function() {
  var disabledFeatures;

  function getFeatures() {
    disabledFeatures = disabledFeatures || fetchDisabledFeatures();
    return disabledFeatures;
  }

  function fetchDisabledFeatures() {
    return ['saveDraft', 'createNewTag', 'replySection'];
  }

  return {
    isEnabled: function(featureName) {
      return ! _.contains(getFeatures(), featureName);
    }
  };
});
