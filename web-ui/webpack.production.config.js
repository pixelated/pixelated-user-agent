var path = require('path');
var webpack = require('webpack');
var publicAssetsWebpack = require('./config/public-assets-webpack');
var protectedAssetsWebpack = require('./config/protected-assets-webpack');
var loaders = require('./config/loaders-webpack');
var aliases = require('./config/alias-webpack');

var commonConfiguration = {
  node: { fs: 'empty' },
  devtool: 'source-map',
  resolve: {
    alias: aliases,
    extensions: ['', '.js']
  },
  module: {
    loaders: loaders
  },
  postcss: {}
};

var commonPlugins = [
  new webpack.optimize.UglifyJsPlugin(),
  new webpack.optimize.DedupePlugin(),
  new webpack.DefinePlugin({
    'process.env': {
      NODE_ENV: JSON.stringify('production')
    }
  })
];

var publicAssets = Object.assign({}, commonConfiguration, {
  entry: {
    'login': './src/login/login.js',
  },
  output: {
    path: path.join(__dirname, 'dist/public'),
    filename: '[name].js',
    publicPath: '/assets/'
  },
  plugins: commonPlugins.concat([ publicAssetsWebpack ])
});

var protectedAssets = Object.assign({}, commonConfiguration, {
  entry: {
    'app': './app/js/index.js',
    'backup_account': './src/backup_account/backup_account.js',
    'sandbox': './app/js/sandbox.js'
  },
  output: {
    path: path.join(__dirname, 'dist/protected'),
    filename: '[name].js',
    publicPath: '/assets/'
  },
  plugins: commonPlugins.concat([ protectedAssetsWebpack ])
});

module.exports = [publicAssets, protectedAssets];
