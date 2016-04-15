describeComponent('page/version', function () {
  'use strict';
  beforeEach(function () {
    this.setupComponent('<div class="version">0.3.1-beta</div>');
  });


  describe('render version on the left nav bar', function () {
    it('should render commit sha and comm', function () {
      expect(this.$node.html()).toContain('version: ');
      expect(this.$node.html()).toContain('ago');
      expect(this.$node.html()).not.toContain('NaN');
    });
  });

});
