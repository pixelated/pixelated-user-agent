define(function() {
'use strict';
  var rawMail = {
    header: {
      to:'jed_waelchi@cummerata.info',
      from:'laurel@hamill.info',
      subject:'Velit aut tempora animi ut nulla esse.',
      date:'2014-06-04T14:41:13-03:00'
    },
    ident:2048,
    tags:['gang_family','garden','nailartaddicts','inbox'],
    status:[],
    textPlainBody: 'Porro quam minus. Doloribus odio vel. Placeat alias sed est assumenda qui esse. Tenetur tempora deserunt est consequatur ducimus laborum. Velit dolor voluptatibus.\n\nRerum repellendus tempore. Aliquam dolores laudantium amet et dolor voluptas. Quod eos magni mollitia et ex. Corrupti quis reprehenderit quasi. Quam cum nobis voluptas accusamus quisquam ut asperiores.\n\nFacilis dicta mollitia non molestiae. Eligendi perspiciatis aut qui eos qui. Laborum cumque odit velit nobis. Cumque quo impedit dignissimos quia.',
    security_casing: {
      locks: [],
      imprints: []
    },
    replying: {
      single: 'laurel@hamil.info',
      all: {
        'to-field': ['laurel@hamil.info'],
        'cc-field': []
      }
    }
  };

  var rawSentMail = {
    'header':{'to':'mariane_dach@davis.info', 'cc': 'duda@la.lu', 'from':'afton_braun@botsford.biz','subject':'Consectetur sit omnis veniam blanditiis.','date':'2014-06-17T11:56:53-03:00'},
    'ident':9359,
    'tags':['photography','sky'],
    'status':['read'],
    textPlainBody:'Illum eos nihil commodi voluptas. Velit consequatur odio quibusdam. Beatae aliquam hic quos.',
    'mailbox': 'SENT',
    replying: {
      single: 'laurel@hamil.info',
      all: {
        'to-field': ['mariane_dach@davis.info'],
        'cc-field': ['duda@la.lu']
      }
    }
  };

  var rawDraftMail = {
    'header':{'to':'mariane_dach@davis.info','from':'afton_braun@botsford.biz','subject':'Consectetur sit omnis veniam blanditiis.','date':'2014-06-17T11:56:53-03:00'},
    'ident':9360,
    'tags':['photography','sky'],
    'status':['read'],
    textPlainBody:'Illum eos nihil commodi voluptas. Velit consequatur odio quibusdam. Beatae aliquam hic quos.',
    'mailbox': 'DRAFTS',
    replying: {
      single: 'afton_braun@botsford.biz',
      all: {
        'to-field': ['afton_braun@botsford.biz'],
        'cc-field': []
      }
    }
  };

  var rawMailInTrash = {
    'header':{'to':'mariane_dach@davis.info','from':'afton_braun@botsford.biz','subject':'Consectetur sit omnis veniam blanditiis.','date':'2014-06-17T11:56:53-03:00'},
    'ident':9360,
    'tags':['photography','sky'],
    'status':['read'],
    textPlainBody:'Illum eos nihil commodi voluptas. Velit consequatur odio quibusdam. Beatae aliquam hic quos.',
    'mailbox': 'TRASH',
    replying: {
      single: 'afton_braun@botsford.biz',
      all: {
        'to-field': ['afton_braun@botsford.biz'],
        'cc-field': []
      }
    }
  };

  var rawReceivedMail = {
    'header':{'to':'stanford@sipes.com','from':'cleve_jaskolski@schimmelhirthe.net','reply_to':'afton_braun@botsford.biz','subject':'Cumque pariatur vel consequuntur deleniti ex.','date':'2014-06-17T05:40:29-03:00'},
    'ident':242,
    'tags':['garden','instalovers','popularpic'],
    'status':['read'],
    textPlainBody: 'Sed est neque tempore. Alias officiis pariatur ullam porro corporis. Tempore eum quia placeat. Sapiente fuga cum.',
    replying: {
      single: 'afton_braun@botsford.biz',
      all: {
        'to-field': ['cleve_jaskolski@schimmelhirthe.net', 'afton_braun@botsford.biz'],
        'cc-field': []
      }
    }

  };

  var rawReceivedWithCCMail = {
    'header':{'to':'stanford@sipes.com','from':'cleve_jaskolski@schimmelhirthe.net','cc':'mariane_dach@davis.info','subject':'Cumque pariatur vel consequuntur deleniti ex.','date':'2014-06-17T05:40:29-03:00'},
    'ident':242,
    'tags':['garden','instalovers','popularpic'],
    'status':['read'],
    'body':'Sed est neque tempore. Alias officiis pariatur ullam porro corporis. Tempore eum quia placeat. Sapiente fuga cum.',
    textPlainBody: 'body',
    replying: {
      single: 'cleve_jaskolski@schimmelhirthe.net',
      all: {
        'to-field': ['cleve_jaskolski@schimmelhirthe.net'],
        'cc-field': ['mariane_dach@davis.info']
      }
    }

  };

  var rawMailWithMultipleTo = {
    'header':{'to':['stanford@sipes.com', 'someoneelse@some-other-domain.tld'],'from':'cleve_jaskolski@schimmelhirthe.net','cc':'mariane_dach@davis.info','subject':'Cumque pariatur vel consequuntur deleniti ex.','date':'2014-06-17T05:40:29-03:00'},
    'ident':242,
    'tags':['garden','instalovers','popularpic'],
    'status':['read'],
    textPlainBody:'Sed est neque tempore. Alias officiis pariatur ullam porro corporis. Tempore eum quia placeat. Sapiente fuga cum.',
    replying: {
      single: 'cleve_jaskolski@schimmelhirthe.net',
      all: {
        'to-field': ['cleve_jaskolski@schimmelhirthe.net', 'someoneelse@some-other-domain.tld'],
        'cc-field': ['mariane_dach@davis.info']
      }
    }

  };

  var simpleTextPlainMail = {
    header: {
      to:'jed_waelchi@cummerata.info',
      from:'laurel@hamill.info',
      subject:'Velit aut tempora animi ut nulla esse.',
      date:'2014-06-04T14:41:13-03:00'
    },
    ident:1,
    tags:['textplain'],
    mailbox: ['inbox'],
    status:[],
    attachments: [],
    textPlainBody: 'Hello Everyone',
    isSentMail: function() { return false; },
    isDraftMail: function() { return false; },
    replyToAddress: function() { return { to: ['laurel@hamill.info'], cc: [] }; },
    replyToAllAddress: function() { return { to: ['laurel@hamill.info'], cc: [] }; },
    isMailMultipartAlternative: function() { return false; },
    availableBodyPartsContentType: function() { return []; },
    getMailPartByContentType: function() { return; }
  };

  var htmlNoEncodingMail = {
    header: {
      to:'jed_waelchi@cummerata.info',
      from:'laurel@hamill.info',
      subject:'Velit aut tempora animi ut nulla esse.',
      content_type: 'multipart/alternative; boundary=asdfghjkl',
      date:'2014-06-04T14:41:13-03:00'
    },
    ident:2,
    tags:['html','noencoding','inbox'],
    status:[],
    textPlainBody: 'Hello everyone!',
    htmlBody: '<DOCTYPE html>\n<body> <div> <p>Hello everyone!</p> </div> </body>',
    isSentMail: function() { return false; },
    isDraftMail: function() { return false; },
    replyToAddress: function() { return { to: ['laurel@hamill.info'], cc: [] }; },
    replyToAllAddress: function() { return { to: ['laurel@hamill.info'], cc: [] }; },
    isMailMultipartAlternative: function () { return true; },
    availableBodyPartsContentType: function () { return ['text/html']; },
    getMailPartByContentType: function () {
      return {
        headers: { 'Content-Type': 'text/html; charset=utf-8' },
        body: '<!DOCTYPE html> <body> <div> <p>Hello everyone!</p> </div> </body>'
      };
    }
  };

  var draftMail = {
    status: [],
    header: {'from': 'jed_waelchi@cummerata.info',
      cc: [],
      bcc: [],
      to: [],
      date: '2015-04-09T18:30:18.998999-03:00',
      subject: 'bla'},
    ident: 'B2432',
    replying: {'single': 'jed_waelchi@cummerata.info',
      all: {
        'to-field': ['jed_waelchi@cummerata.info'],
        'cc-field': []
      }
    },
    attachments: [],
    textPlainBody: 'bla',
    tags: [],
    htmlBody: null,
    mailbox: 'drafts',
    security_casing: {'locks': [],
      imprints: [{'state': 'no_signature_information'}]
    },
    isSentMail: function() { return false; },
    isDraftMail: function() { return false; },
    replyToAddress: function() { return { to: ['jed_waelchi@cummerata.info'], cc: [] }; },
    replyToAllAddress: function() { return { to: ['jed_waelchi@cummerata.info'], cc: [] }; },
    isMailMultipartAlternative: function () { return false; },
    availableBodyPartsContentType: function () { return []; },
    getMailPartByContentType: function () { return; }
  };

  var withAttachments = {
    header: {
      to:'jed_waelchi@cummerata.info',
      from:'laurel@hamill.info',
      subject:'Velit aut tempora animi ut nulla esse.',
      date:'2014-06-04T14:41:13-03:00'
    },
    ident:1,
    tags:['textplain'],
    mailbox: ['inbox'],
    status:[],
    textPlainBody: 'Hello Everyone',
    isSentMail: function() { return false; },
    isDraftMail: function() { return false; },
    replyToAddress: function() { return { to: ['laurel@hamill.info'], cc: [] }; },
    replyToAllAddress: function() { return { to: ['laurel@hamill.info'], cc: [] }; },
    isMailMultipartAlternative: function() { return false; },
    availableBodyPartsContentType: function() { return []; },
    getMailPartByContentType: function() { return; },
    attachments: [{
      ident: '912ec803b2ce49e4a541068d495ab570',
      name: 'filename.txt',
      encoding: 'base64',
      'content-type': 'text/plain'
    }]
  };

  var testData = {
    rawMail: {
      mail: rawMail,
      sent: rawSentMail,
      draft: rawDraftMail,
      trash: rawMailInTrash,
      received: rawReceivedMail,
      receivedWithCC: rawReceivedWithCCMail,
      rawMailWithMultipleTo: rawMailWithMultipleTo
    },
    parsedMail: {
      simpleTextPlain: simpleTextPlainMail,
      html: htmlNoEncodingMail,
      draft: draftMail,
      withAttachments: withAttachments
    }
  };

  return function () {
    return _.cloneDeep(testData);
  };
});
