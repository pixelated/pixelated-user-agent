describeComponent('page/logout_shortcut', function () {
  'use strict';

  describe('logout icon', function () {
    var features;

    beforeEach(function() {
      features = require('features');
    });

    it('should provide logout icon if logout is enabled', function () {
      spyOn(features, 'isLogoutEnabled').and.returnValue(true);

      this.setupComponent('<ul id="logout-shortcut" class="shortcuts">, {}');

      var logout_icon = this.component.$node.find('a')[0];
      expect(logout_icon).toExist();
      expect(logout_icon.innerHTML).toContain('i class="fa fa-sign-out"></i>');
      //expect(logout_icon.innerHTML).toContain('foobar')
    });

    it('should not provide logout icon if logout is disabled', function () {
      spyOn(features, 'isLogoutEnabled').and.returnValue(false);

      this.setupComponent('<ul id="logout-shortcut" class="shortcuts">, {}');

      var logout_icon = this.component.$node.find('a')[0];
      expect(logout_icon).not.toExist();
    });
  });
});