describeComponent('page/logout', function () {
  'use strict';

  describe('logout link', function () {
    var features;

    beforeEach(function() {
      features = require('features');
    });

    it('should provide logout link if logout is enabled', function () {
      spyOn(features, 'isLogoutEnabled').and.returnValue(true);

      this.setupComponent('<nav id="logout"></nav>', {});

      var logout_link = this.component.$node.find('a')[0];
      expect(logout_link).toExist();
      expect(logout_link.href).toMatch('test/logout/url');
    });

    it('should not provide logout link if disabled', function() {
      spyOn(features, 'isLogoutEnabled').and.returnValue(false);

      this.setupComponent('<nav id="logout"></nav>', {});

      var logout_link = this.component.$node.find('a')[0];
      expect(logout_link).not.toExist();
    });

    it('should render logout in collapsed nav bar if logout is enabled', function() {
      spyOn(features, 'isLogoutEnabled').and.returnValue(true);

      this.setupComponent('<ul id="logout-shortcuts" class="shortcuts"></ul>', {});

      var logout_icon = this.component.$node.find('a')[0];
      expect(logout_icon).toExist();
      expect(logout_icon.innerHTML).toContain('<div class="fa fa-sign-out"></div>');
    });
  });
});

