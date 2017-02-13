var path = require('path');
var webpack = require('webpack');
var copyWebpack = require('./config/copy-webpack');
var loaders = require('./config/loaders-webpack');
var aliases = require('./config/alias-webpack');

module.exports = {
  entry: {
    app: './app/js/index.js',
    backup_account: './src/backup_account/backup_account.js',
    login: './src/login/login.js',
    sandbox: './app/js/sandbox.js'
  },
  node: { fs: 'empty' },
  output: {
    path: path.join(__dirname, 'dist'),
    filename: '[name].js',
    publicPath: '/assets/'
  },
  resolve: {
    alias: aliases,
    extensions: ['', '.js']
  },
  module: {
    loaders: loaders
  },
  plugins: [
    new webpack.optimize.UglifyJsPlugin(),
    new webpack.optimize.DedupePlugin(),
    new webpack.DefinePlugin({
      'process.env': {
        NODE_ENV: JSON.stringify('production')
      }
    }),
    copyWebpack
  ]
}
