var path = require('path');
var webpack = require('webpack');
var copyWebpack = require('./config/copy-webpack');
var aliases = require('./config/alias-webpack');

module.exports = {
  resolve: {
    alias: aliases,
    extensions: ['', '.js']
  },
  externals: {
    'react/lib/ExecutionEnvironment': true,
    'react/addons': true,
    'react/lib/ReactContext': 'window'
  },
  module: {
    loaders: [
      {
        test: /\.js$/,
        exclude: /(node_modules|bower_components)/,
        loader: 'babel',
        query: { presets: ['es2015', 'react']}
      },
      {
        test: /\.scss|css$/,
        loader: "css-loader!sass-loader"
      },
      {
        test: /\.json$/,
        loader: "json-loader"
      }
    ]
  }
}
