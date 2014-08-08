define(['features'],
  function(features) {

    function withFeatureToggle(componentName, behaviorForFeatureOff) {
      return function() {

        this.around('initialize', _.bind(function(basicInitialize) {
          if(features.isEnabled(componentName)) {
            return basicInitialize(arguments[1], arguments[2]);
          }
          else if (behaviorForFeatureOff){
            behaviorForFeatureOff.bind(this).call();
          }
        }, this));
      };
    }

    return withFeatureToggle;

});
