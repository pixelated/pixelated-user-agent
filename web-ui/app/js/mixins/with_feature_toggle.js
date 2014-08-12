define(['features'],
  function(features) {

    function withFeatureToggle(componentName, behaviorForFeatureOff) {
      return function() {

        this.around('initialize', _.bind(function(basicInitialize, node, attrs) {
          if(features.isEnabled(componentName)) {
            return basicInitialize(node, attrs);
          }
          else if (behaviorForFeatureOff){
            behaviorForFeatureOff.call(this);

            return this;
          }
        }, this));
      };
    }

    return withFeatureToggle;

});
