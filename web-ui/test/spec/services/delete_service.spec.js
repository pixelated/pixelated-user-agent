/*global jasmine */
/*global Pixelated */

describeComponent('services/delete_service', function () {
  'use strict';

  var i18n;

  beforeEach( function () {
    setupComponent();
    i18n = require('views/i18n');
  });

  var mailWithoutTrashTag = {
    ident: 42,
    isInTrash: function() { return false; },
    tags: ['inbox', 'test']
  };

  var mailWithTrashTag = {
    ident: 34,
    isInTrash: function() { return true; },
    tags: ['inbox', 'test', 'trash']
  };

  it('add Trash tag when deleting an email that does not have it', function () {
    var mailDeleteEvent = spyOnEvent(document, Pixelated.events.mail.delete);
    var openNoMessageSelectedEvent = spyOnEvent(document, Pixelated.events.dispatchers.rightPane.openNoMessageSelected);

    this.component.trigger(document, Pixelated.events.ui.mail.delete, {mail: mailWithoutTrashTag});

    var expectedDeleteEventData = {
      mail: mailWithoutTrashTag,
      successMessage: i18n('Your message was moved to trash!')
    };

    expect(mailDeleteEvent).toHaveBeenTriggeredOnAndWith(document, expectedDeleteEventData);
  });

  it('removes permanently email that has Trash tag', function(){
    var mailDeleteEvent = spyOnEvent(document, Pixelated.events.mail.delete);
    var openNoMessageSelectedEvent = spyOnEvent(document, Pixelated.events.dispatchers.rightPane.openNoMessageSelected);

    this.component.trigger(document, Pixelated.events.ui.mail.delete, {mail: mailWithTrashTag});

    var expectedDeleteEventData = {
      mail: mailWithTrashTag,
      successMessage: i18n('Your message was permanently deleted!')
    };

    expect(mailDeleteEvent).toHaveBeenTriggeredOnAndWith(document, expectedDeleteEventData );
  });

});
