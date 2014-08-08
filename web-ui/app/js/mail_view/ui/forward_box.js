/*global Pixelated */
/*global _ */

define(
  [
    'flight/lib/component',
    'helpers/view_helper',
    'mixins/with_hide_and_show',
    'mixins/with_compose_inline',
    'page/events',
    'views/i18n'
  ],

  function (defineComponent, viewHelper, withHideAndShow, withComposeInline, events, i18n) {
    'use strict';

    return defineComponent(forwardBox, withHideAndShow, withComposeInline);

    function forwardBox() {
      var fwd = function(v) { return i18n('Fwd: ') + v; };

      this.fetchTargetMail = function (ev) {
        this.trigger(document, events.mail.want, { mail: this.attr.ident, caller: this });
      };

      this.setupForwardBox = function() {
        var mail = this.attr.mail;
        this.attr.subject = fwd(mail.header.subject);

        this.renderInlineCompose('forward-box', {
          subject: this.attr.subject,
          recipients: { to: [], cc: []},
          body: viewHelper.quoteMail(mail)
        });

        this.on(this.select('subjectDisplay'), 'click', this.showSubjectInput);
        this.select('recipientsDisplay').hide();
        this.select('recipientsFields').show();
      };

      this.showSubjectInput = function() {
        this.select('subjectDisplay').hide();
        this.select('subjectInput').show();
        this.select('subjectInput').focus();
      };

      this.buildMail = function(tag) {
        var builder = this.builtMail(tag).subject(this.select('subjectInput').val());

        var headersToFwd = ['bcc', 'cc', 'date', 'from', 'message_id', 'reply_to', 'sender', 'to'];
        var header = this.attr.mail.header;
        _.each(headersToFwd, function (h) {
          if (!_.isUndefined(header[h])) {
            builder.header('resent_' + h, header[h]);
          }
        });

        return builder.build();
      };

      this.after('initialize', function () {
        this.setupForwardBox();
      });
    }
  }
);
