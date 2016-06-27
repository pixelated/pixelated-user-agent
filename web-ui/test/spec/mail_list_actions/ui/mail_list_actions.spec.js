describeComponent('mail_list_actions/ui/mail_list_actions', function () {
  'use strict';
  var mailListActionsContainer;
  var i18n;
  describe('post initialization', function () {
    beforeEach(function () {
      this.setupComponent();
      i18n = require('views/i18n');
      mailListActionsContainer = $('<input>', { id: 'delete-selected'});
    });

    it('should render button text', function () {
      $(document).trigger(Pixelated.events.ui.tag.select, {tag: 'inbox'});

      expect(this.component.$node.html()).toMatch('<li><input type="button" id="delete-selected" value="' + i18n.t('Delete') + '" disabled="disabled"></li>');
    });

    it('should render button text delete permanently if tag trash', function () {
      $(document).trigger(Pixelated.events.ui.tag.select, {tag: 'trash'});
      expect(this.component.$node.html()).toMatch('<li><input type="button" id="delete-selected" value="Delete Permanently" disabled="disabled"></li>');
    });

    it('should render button delete permanently if url contains trash tag', function () {
      var urlParams = require('page/router/url_params');
      spyOn(urlParams, 'getTag').and.returnValue('trash');

      this.setupComponent();

      expect(this.component.$node.html()).toMatch('<li><input type="button" id="delete-selected" value="Delete Permanently" disabled="disabled"></li>');
    });

    it('should render move to inbox if on trash', function () {
      var urlParams = require('page/router/url_params');
      spyOn(urlParams, 'getTag').and.returnValue('trash');

      this.setupComponent();

      expect(this.component.$node.html()).toMatch('<li><input type="button" id="recover-selected" value="Move to Inbox" disabled="disabled"></li>');
    });

    it('should not render move to inbox if on trash', function () {
      var urlParams = require('page/router/url_params');
      spyOn(urlParams, 'getTag').and.returnValue('inbox');

      this.setupComponent();

      expect(this.component.$node.html()).not.toMatch('<li><input type="button" id="recover-selected" value="Move to Inbox" disabled="disabled"></li>');
    });
  });
});

