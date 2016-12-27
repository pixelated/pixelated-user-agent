var path = require('path')

module.exports = {
  entry: './app/js/index.js',
  output: {
    path: path.join(__dirname, '/app/js/'),
    filename: 'bundle.js',
    publicPath: '/assets/js/'
  },
  resolve: {
    alias: {
      'js': path.join(__dirname, '/app/js'),
      'flight': path.join(__dirname, '/app/bower_components/flight'),
      'mail_list': path.join(__dirname, '/app/js/mail_list'),
      'page': path.join(__dirname, '/app/js/page'),
      'feedback': path.join(__dirname, '/app/js/feedback'),
      'DOMPurify': 'dompurify',
      'i18nextXHRBackend': 'i18next-xhr-backend',
      'i18nextBrowserLanguageDetector': 'i18next-browser-languagedetector',
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
      'user_settings': path.join(__dirname, '/app/js/user_settings')
    },
    extensions: ['', '.js']
  },
  module: {
    loaders: [
      {
        test: /\.js$/,
        exclude: /(node_modules|bower_components)/,
        loader: 'babel',
        query: { presets: ['es2015']}
      }
    ]
  }
}
