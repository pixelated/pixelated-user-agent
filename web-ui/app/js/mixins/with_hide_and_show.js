define(function(require) {

  function withHideAndShow() {
    this.hide = function () {
      this.$node.hide();
    };
    this.show = function () {
      this.$node.show();
    };
  }

  return withHideAndShow;

});
