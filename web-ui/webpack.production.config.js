var path = require('path');
var webpack = require('webpack');
var CopyWebpackPlugin = require('copy-webpack-plugin');

module.exports = {
  entry: './app/js/index.js',
  node: { fs: 'empty' },
  output: {
    path: path.join(__dirname, '/dist/'),
    filename: 'app.min.js',
    publicPath: '/assets/'
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
        loader: 'babel',
        query: { presets: ['es2015']}
      }
    ]
  },
  plugins: [
    new webpack.optimize.UglifyJsPlugin(),
    new webpack.optimize.DedupePlugin(),
    new CopyWebpackPlugin([
      { context: 'app/', from: '404.html' },
      { context: 'app/', from: 'index.html' },
      { context: 'app/', from: 'css/*' },
      { context: 'app/', from: 'fonts/*' },
      { context: 'app/', from: 'locales/**/*' },
      { context: 'app/', from: 'bower_components/font-awesome/fonts/*' },
      {
        context: 'app/',
        from: 'bower_components/font-awesome/css/font-awesome.min.css',
        to: 'bower_components/font-awesome/css'
      },
      {
        context: 'app/',
        from: 'bower_components/jquery-file-upload/css/jquery.fileupload.css',
        to: 'bower_components/jquery-file-upload/css'
      },
      {
        context: 'app/',
        from: 'bower_components/modernizr/modernizr.js',
        to: 'bower_components/modernizr'
      },
      {
        context: 'app/',
        from: 'bower_components/lodash/dist/lodash.min.js',
        to: 'bower_components/lodash/dist'
      },
      {
        context: 'app/',
        from: 'bower_components/jquery/dist/jquery.min.js',
        to: 'bower_components/jquery/dist'
      },
      {
        context: 'app/',
        from: 'bower_components/jquery-ui/jquery-ui.min.js',
        to: 'bower_components/jquery-ui'
      },
      {
        context: 'app/',
        from: 'bower_components/jquery-file-upload/js/jquery.fileupload.js',
        to: 'bower_components/jquery-file-upload/js'
      },
      {
        context: 'app/',
        from: 'bower_components/handlebars/handlebars.min.js',
        to: 'bower_components/handlebars'
      },
      {
        context: 'app/',
        from: 'bower_components/typeahead.js/dist/typeahead.bundle.min.js',
        to: 'bower_components/typeahead.js/dist'
      },
      {
        context: 'app/',
        from: 'bower_components/iframe-resizer/js/iframeResizer.min.js',
        to: 'bower_components/iframe-resizer/js'
      },
      {
        context: 'app/',
        from: 'bower_components/foundation/js/foundation.js',
        to: 'bower_components/foundation/js'
      },
      {
        context: 'app/',
        from: 'bower_components/foundation/js/foundation/foundation.reveal.js',
        to: 'bower_components/foundation/js/foundation'
      },
      {
        context: 'app/',
        from: 'bower_components/foundation/js/foundation/foundation.offcanvas.js',
        to: 'bower_components/foundation/js/foundation'
      },
      {
        context: 'app/',
        from: 'js/foundation/initialize_foundation.js',
        to: 'js/foundation'
      }
    ])
  ]
}
