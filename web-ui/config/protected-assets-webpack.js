var CopyWebpackPlugin = require('copy-webpack-plugin');

module.exports = new CopyWebpackPlugin([
  { context: 'app/', from: '404.html' },
  { context: 'app/', from: 'index.html' },
  { context: 'app/', from: 'sandbox.html' },
  { context: 'app/', from: 'css/*' },
  { context: 'src/account_recovery/', from: 'account_recovery.html' },
  { context: 'src/backup_account/', from: 'backup_account.html' },
  { context: 'app/bower_components/font-awesome/', from: 'fonts/*' },
  { context: 'app/bower_components/font-awesome/', from: 'css/font-awesome.min.css', to: 'css' },
  { context: 'app/bower_components/jquery-file-upload/', from: 'css/jquery.fileupload.css', to: 'css' },
  { context: 'app/bower_components/modernizr/', from: 'modernizr.js' },
  { context: 'app/bower_components/lodash/dist/', from: 'lodash.min.js' },
  { context: 'app/bower_components/jquery/dist/', from: 'jquery.min.js' },
  { context: 'app/bower_components/jquery-ui/', from: 'jquery-ui.min.js' },
  { context: 'app/bower_components/jquery-file-upload/js/', from: 'jquery.fileupload.js' },
  { context: 'app/bower_components/handlebars/', from: 'handlebars.min.js' },
  { context: 'app/bower_components/typeahead.js/dist/', from: 'typeahead.bundle.min.js' },
  { context: 'app/bower_components/iframe-resizer/js/', from: 'iframeResizer.min.js' },
  { context: 'app/bower_components/iframe-resizer/js/', from: 'iframeResizer.contentWindow.min.js' },
  { context: 'app/bower_components/foundation/js/', from: 'foundation.js' },
  { context: 'app/bower_components/foundation/js/foundation/', from: 'foundation.reveal.js' },
  { context: 'app/bower_components/foundation/js/foundation/', from: 'foundation.offcanvas.js' },
  { context: 'app/js/foundation/', from: 'initialize_foundation.js' }
])
