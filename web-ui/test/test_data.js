/*global _ */
'use strict';

define(function() {
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
    body: 'Porro quam minus. Doloribus odio vel. Placeat alias sed est assumenda qui esse. Tenetur tempora deserunt est consequatur ducimus laborum. Velit dolor voluptatibus.\n\nRerum repellendus tempore. Aliquam dolores laudantium amet et dolor voluptas. Quod eos magni mollitia et ex. Corrupti quis reprehenderit quasi. Quam cum nobis voluptas accusamus quisquam ut asperiores.\n\nFacilis dicta mollitia non molestiae. Eligendi perspiciatis aut qui eos qui. Laborum cumque odit velit nobis. Cumque quo impedit dignissimos quia.',
    security_casing: {
      locks: [],
      imprints: []
    }
  };

  var rawSentMail = {
    'header':{'to':'mariane_dach@davis.info', 'cc': 'duda@la.lu', 'from':'afton_braun@botsford.biz','subject':'Consectetur sit omnis veniam blanditiis.','date':'2014-06-17T11:56:53-03:00'},
    'ident':9359,
    'tags':['photography','sky'],
    'status':['read'],
    'body':'Illum eos nihil commodi voluptas. Velit consequatur odio quibusdam. Beatae aliquam hic quos.',
    'mailbox': 'SENT'
  };

  var rawDraftMail = {
    'header':{'to':'mariane_dach@davis.info','from':'afton_braun@botsford.biz','subject':'Consectetur sit omnis veniam blanditiis.','date':'2014-06-17T11:56:53-03:00'},
    'ident':9360,
    'tags':['photography','sky'],
    'status':['read'],
    'body':'Illum eos nihil commodi voluptas. Velit consequatur odio quibusdam. Beatae aliquam hic quos.',
    'mailbox': 'DRAFTS'
  };

  var rawRecievedMail = {
    'header':{'to':'stanford@sipes.com','from':'cleve_jaskolski@schimmelhirthe.net','reply_to':'afton_braun@botsford.biz','subject':'Cumque pariatur vel consequuntur deleniti ex.','date':'2014-06-17T05:40:29-03:00'},
    'ident':242,
    'tags':['garden','instalovers','popularpic'],
    'status':['read'],
    'body':'Sed est neque tempore. Alias officiis pariatur ullam porro corporis. Tempore eum quia placeat. Sapiente fuga cum.'
  };

  var rawRecievedWithCCMail = {
    'header':{'to':'stanford@sipes.com','from':'cleve_jaskolski@schimmelhirthe.net','cc':'mariane_dach@davis.info','subject':'Cumque pariatur vel consequuntur deleniti ex.','date':'2014-06-17T05:40:29-03:00'},
    'ident':242,
    'tags':['garden','instalovers','popularpic'],
    'status':['read'],
    'body':'Sed est neque tempore. Alias officiis pariatur ullam porro corporis. Tempore eum quia placeat. Sapiente fuga cum.'
  };

  var rawMailWithMultipleTo = {
    'header':{'to':['stanford@sipes.com', 'someoneelse@some-other-domain.tld'],'from':'cleve_jaskolski@schimmelhirthe.net','cc':'mariane_dach@davis.info','subject':'Cumque pariatur vel consequuntur deleniti ex.','date':'2014-06-17T05:40:29-03:00'},
    'ident':242,
    'tags':['garden','instalovers','popularpic'],
    'status':['read'],
    'body':'Sed est neque tempore. Alias officiis pariatur ullam porro corporis. Tempore eum quia placeat. Sapiente fuga cum.'
  };

  var rawMultipartMail = {
    header: {
      to:'multipart@multipart.info',
      from:'laurel@hamill.info',
      subject:'multipart email with text/plain and text/html',
      content_type: 'multipart/alternative; boundary=asdfghjkl',
      date:'2014-06-04T14:41:13-03:00'
    },
    ident: 11,
    tags:['multipart','inbox'],
    status:[],
    body: '--asdfghjkl\n' +
          'Content-Type: text/plain;\n' +
          '\n' +
          'Hello everyone!\n' +
          '--asdfghjkl\n' +
          'Content-Type: text/html;\n' +
          'Content-Transfer-Encoding: quoted-printable\n' +
          '\n' +
          '<p><b>Hello everyone!</b></p>\n' +
          '--asdfghjkl--\n'
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
    body: 'Hello Everyone',
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
    body: '--asdfghjkl\nContent-Type: text/html; charset=utf8\n\n<DOCTYPE html>\n<body> <div> <p>Hello everyone!</p> </div> </body>\n--asdfghjkl--\n',
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

  var htmlQuotedPrintableMail = {
    header: {
      to:'jed_waelchi@cummerata.info',
      from:'laurel@hamill.info',
      subject:'Velit aut tempora animi ut nulla esse.',
      content_type: 'multipart/alternative; boundary=asdfghjkl',
      date:'2014-06-04T14:41:13-03:00'
    },
    ident:3,
    tags:['html','quotedprintable','inbox'],
    status:[],
    body: '--asdfghjkl\nContent-Type: text/html; charset=utf8\nContent-Transfer-Encoding: quoted-printable\n\n<DOCTYPE html>\n<body> <div style=3D"border: 5px;"> <p>Hello everyone!</p> </div> </body>\n--asdfghjkl--\n',
    isSentMail: function() { return false; },
    isDraftMail: function() { return false; },
    replyToAddress: function() { return { to: ['laurel@hamill.info'], cc: [] }; },
    replyToAllAddress: function() { return { to: ['laurel@hamill.info'], cc: [] }; },
    isMailMultipartAlternative: function () { return true; },
    availableBodyPartsContentType: function () { return ['text/html']; },
    getMailPartByContentType: function () {
      return {
        headers: {
          'Content-Type': 'text/html; charset=utf-8',
          'Content-Transfer-Encoding': 'quoted-printable'},
        body: '<!DOCTYPE html> <body> <div> <p style=3D"border: 5px;">Hello everyone!</p> </div> </body>'
      };
    }
  };

  var testData = {
    rawMail: {
      mail: rawMail,
      sent: rawSentMail,
      draft: rawDraftMail,
      recieved: rawRecievedMail,
      recievedWithCC: rawRecievedWithCCMail,
      rawMailWithMultipleTo: rawMailWithMultipleTo,
      multipart: rawMultipartMail
    },
    parsedMail: {
      simpleTextPlain: simpleTextPlainMail,
      html: htmlNoEncodingMail,
      htmlQuotedPrintable: htmlQuotedPrintableMail
    }
  };

  return function () {
    return _.cloneDeep(testData);
  };
});
