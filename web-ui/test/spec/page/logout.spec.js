/*global Pixelated */

describeComponent('page/logout', function () {
  'use strict';

  describe('logout link', function () {
    var features;

    beforeEach(function() {
      features = require('features');
    });

    it('should provide logout link if logout is enabled', function () {
      spyOn(features, 'isLogoutEnabled').and.returnValue(true);

      this.setupComponent('<div id="logout"></div>', {});

      var logout_link = this.component.$node.find('a')[0];
      expect(logout_link).toExist();
      expect(logout_link.href).toMatch('test/logout/url');
    });

    it('should not provide logout link if disabled', function() {
      spyOn(features, 'isLogoutEnabled').and.returnValue(false);

      this.setupComponent('<div id="logout"></div>', {});

      var logout_link = this.component.$node.find('a')[0];
      expect(logout_link).not.toExist();
    });
  });
});

