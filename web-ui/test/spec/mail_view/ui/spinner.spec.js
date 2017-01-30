describeComponent('mail_view/ui/spinner', function () {
  'use strict';

  describe('spinner on initialization', function () {

    it('should render the spinner svg', function () {
      this.setupComponent();
      expect(this.$node.html()).toMatch('<svg id="spinner"');
    });
  });
});
