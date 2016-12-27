var path = require('path')

module.exports = {
  resolve: {
    alias: {
      'mail_list': path.join(__dirname, '/app/js/mail_list'),
      'page': path.join(__dirname, '/app/js/page'),
      'feedback': path.join(__dirname, '/app/js/feedback'),
      'flight': path.join(__dirname, '/app/bower_components/flight'),
      'DOMPurify': path.join(__dirname, '/app/bower_components/DOMPurify/dist/purify.min'),
      'he': path.join(__dirname, '/app/bower_components/he/he'),
      'hbs': path.join(__dirname, '/app/js/generated/hbs'),
      'helpers': path.join(__dirname, '/app/js/helpers'),
      'lib': path.join(__dirname, '/app/js/lib'),
      'views': path.join(__dirname, '/app/js/views'),
      'tags': path.join(__dirname, '/app/js/tags'),
      'mail_list_actions': path.join(__dirname, '/app/js/mail_list_actions'),
      'user_alerts': path.join(__dirname, '/app/js/user_alerts'),
      'mail_view': path.join(__dirname, '/app/js/mail_view'),
      'dispatchers': path.join(__dirname, '/app/js/dispatchers'),
      'services': path.join(__dirname, '/app/js/services'),
      'mixins': path.join(__dirname, '/app/js/mixins'),
      'search': path.join(__dirname, '/app/js/search'),
      'foundation': path.join(__dirname, '/app/js/foundation'),
      'features': path.join(__dirname, '/app/js/features/features'),
      'i18next': path.join(__dirname, '/app/bower_components/i18next/i18next'),
      'i18nextXHRBackend': path.join(__dirname, '/app/bower_components/i18next-xhr-backend/i18nextXHRBackend'),
      'i18nextBrowserLanguageDetector': path.join(__dirname, '/app/bower_components/i18next-browser-languagedetector/i18nextBrowserLanguageDetector'),
      'quoted-printable': path.join(__dirname, '/app/bower_components/quoted-printable'),
      'utf8': path.join(__dirname, '/app/bower_components/utf8'),
      'user_settings': path.join(__dirname, '/app/js/user_settings')
    },
    moduleDirectories: ['app/js']
  }
}
