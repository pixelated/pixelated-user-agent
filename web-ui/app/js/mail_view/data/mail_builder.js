/*global _ */

define(['services/model/mail'], function (mailModel) {
  'use strict';

  var mail;

  function recipients(mail, place, v) {
    if (v !== '' && !_.isUndefined(v)) {
      if(_.isArray(v)) {
        mail[place] = v;
      } else {
        mail[place] = v.split(' ');
      }
    } else {
      mail[place] = [];
    }
  }

  return {
    newMail: function(ident) {
      ident = _.isUndefined(ident) ? '' : ident;

      mail = {
        header: {
          to: [],
          cc: [],
          bcc: [],
          from: undefined,
          subject: ''
        },
        tags: [],
        body: '',
        ident: ident
      };
      return this;
    },

    subject: function (subject) {
      mail.header.subject = subject;
      return this;
    },

    body: function(body) {
      mail.body = body;
      return this;
    },

    to: function (to) {
      recipients(mail.header, 'to', to);
      return this;
    },

    cc: function (cc) {
      recipients(mail.header, 'cc', cc);
      return this;
    },

    bcc: function (bcc) {
      recipients(mail.header, 'bcc', bcc);
      return this;
    },

    header: function(name, value) {
      mail.header[name] = value;
      return this;
    },

    tag: function(tag) {
      if(_.isUndefined(tag)) { tag = 'drafts'; }
      mail.tags.push(tag);
      return this;
    },

    build: function() {
      return mailModel.create(mail);
    }
  };
});
