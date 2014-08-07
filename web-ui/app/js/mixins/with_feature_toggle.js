define(['features'],
  function(features) {

    function withFeatureToggle(componentName) {
      return function() {

        this.around('initialize', function(basicInitialize) {
          if(features.isEnabled(componentName)) {
            return basicInitialize(arguments[1], arguments[2]);
          }
        });
      };
    }

    return withFeatureToggle;

});
