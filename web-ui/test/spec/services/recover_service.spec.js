describeComponent('services/recover_service', function () {
  'use strict';

  var i18n;

  beforeEach( function () {
    this.setupComponent();
    i18n = require('views/i18n');
  });

  var mail1 = {
    ident: 42,
    isInTrash: function() { return false; }
  };

  var mail2 = {
    ident: 34,
    isInTrash: function() { return true; }
  };

  it('moves selected emails from trash back to inbox', function () {
    var mailRecoverManyEvent = spyOnEvent(document, Pixelated.events.mail.recoverMany);
    this.component.trigger(document, Pixelated.events.ui.mail.recoverMany, {checkedMails: {mail1: mail1, mail2: mail2}});

    var expectedRecoverManyEventData = {
      mails: [mail1, mail2],
      successMessage: i18n.t('Your messages were moved to inbox!')
    };

    expect(mailRecoverManyEvent).toHaveBeenTriggeredOnAndWith(document, expectedRecoverManyEventData);
  });
});
