'use strict';

define(
  [
    'mail_list/ui/mail_items/generic_mail_item',
    'mail_list/ui/mail_items/draft_item',
    'mail_list/ui/mail_items/sent_item'
  ],
  function (GenericMailItem, DraftItem, SentItem) {

    var MAIL_ITEM_TYPE = {
      'drafts': DraftItem,
      'sent': SentItem
    };

    var createAndAttach = function (nodeToAttachTo, mail, currentMailIdent, currentTag, isChecked) {
      var mailItemContainer = $('<li>', { id: 'mail-' + mail.ident});
      nodeToAttachTo.append(mailItemContainer);

      var mailToCreate;
      if(currentTag === 'all'){
        mailToCreate = detectMailType(mail);
      } else {
        mailToCreate = MAIL_ITEM_TYPE[currentTag] || GenericMailItem;
      }
      mailToCreate.attachTo(mailItemContainer, {
        mail: mail,
        selected: mail.ident === currentMailIdent,
        tag: currentTag,
        isChecked: isChecked
      });

    };

    var detectMailType = function(mail) {
      if(_.include(mail.tags, 'drafts')) {
        return MAIL_ITEM_TYPE['drafts'];
      } else if(_.include(mail.tags, 'sent')) {
        return MAIL_ITEM_TYPE['sent'];
      } else {
        return GenericMailItem;
      };
    };

    return {
      createAndAttach: createAndAttach
    };
  }
);
