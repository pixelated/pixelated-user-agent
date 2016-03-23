describeComponent('page/logout', function () {
  'use strict';

  describe('logout link', function () {
    var features;

    beforeEach(function() {
      features = require('features');
    });

    it('should provide logout form if logout is enabled', function () {
      spyOn(features, 'isLogoutEnabled').and.returnValue(true);

      this.setupComponent('<nav id="logout"></nav>', {});

      var logout_form = this.component.$node.find('form')[0];
      expect(logout_form).toExist();
      expect(logout_form.action).toMatch('test/logout/url');
      expect(logout_form.method).toMatch('post');
    });

    it('should not provide logout form if logout is disabled', function () {
      spyOn(features, 'isLogoutEnabled').and.returnValue(false);

      this.setupComponent('<nav id="logout"></nav>', {});

      var logout_form = this.component.$node.find('form')[0];
      expect(logout_form).not.toExist();
    });

    it('should provide csrf token if logout is enabled', function () {
      spyOn(features, 'isLogoutEnabled').and.returnValue(true);
      document.cookie = 'XSRF-TOKEN=ff895ffc45a4ce140bfc5dda6c61d232; i18next=en-us';

      this.setupComponent('<nav id="logout"></nav>', {});

      var logout_input = this.component.$node.find('input')[0];
      expect(logout_input).toExist();
      expect(logout_input.value).toEqual('ff895ffc45a4ce140bfc5dda6c61d232');
      expect(logout_input.type).toEqual('hidden');
    });

    it('should not provide csrf token if logout is disabled', function () {
      spyOn(features, 'isLogoutEnabled').and.returnValue(false);

      this.setupComponent('<nav id="logout"></nav>', {});

      var logout_input = this.component.$node.find('input')[0];
      expect(logout_input).not.toExist();
    });

    xit('should render logout in collapsed nav bar if logout is enabled', function() {
      spyOn(features, 'isLogoutEnabled').and.returnValue(true);

      this.setupComponent('<ul id="logout-shortcuts" class="shortcuts"></ul>', {});

      var logout_icon = this.component.$node.find('a')[0];
      expect(logout_icon).toExist();
      expect(logout_icon.innerHTML).toContain('<div class="fa fa-sign-out"></div>');
    });

    it('should submit logout form if logout is enabled', function () {
      spyOn(features, 'isLogoutEnabled').and.returnValue(true);

      this.setupComponent('<nav id="logout"></nav>', {});

      var logout_form = this.component.$node.find('form')[0];
      spyOn(logout_form, 'submit');

      this.component.$node.click();

      expect(logout_form.submit).toHaveBeenCalled();
    });


  });
});
