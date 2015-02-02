describeComponent('mail_list_actions/ui/mail_list_actions', function () {
  'use strict';
  var mailListActionsContainer;

  describe('post initialization', function () {
    beforeEach(function () {
      this.setupComponent();
      mailListActionsContainer = $('<input>', { id: 'delete-selected'});
    });

    it('should render button text', function () {
      $(document).trigger(Pixelated.events.ui.tag.select, {tag: 'inbox'});
      
      expect(this.component.$node.html()).toMatch('<li><input type="button" id="delete-selected" value="Delete" disabled="disabled"></li>');
    });

    it('should render button text delete permanently if tag trash', function () {
      $(document).trigger(Pixelated.events.ui.tag.select, {tag: 'trash'});
      
      expect(this.component.$node.html()).toMatch('<li><input type="button" id="delete-selected" value="Delete permanently" disabled="disabled"></li>');
    });
    
    it('should render button delete permanently if url contains trash tag', function () {
      var urlParams = require('page/router/url_params');
      spyOn(urlParams, 'getTag').and.returnValue('trash');

      this.setupComponent();

      expect(this.component.$node.html()).toMatch('<li><input type="button" id="delete-selected" value="Delete permanently" disabled="disabled"></li>');
    });
  });
});

