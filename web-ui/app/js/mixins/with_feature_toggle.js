define(['lib/features'],
  function(features) {

    function withFeatureToggle(componentName) {
      return function() {

        var defaultToggle = {enabled: true};

        this.around('initialize', function(basicInitialize) {
          var featureToggle = features[componentName] || defaultToggle;
          if(featureToggle.enabled) {
            basicInitialize(arguments[1], arguments[2]);
          }
        });
      };
    }

    return withFeatureToggle;

});
