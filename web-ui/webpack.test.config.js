var path = require('path');
var webpack = require('webpack');
var aliases = require('./config/alias-webpack');
var nodeExternals = require('webpack-node-externals');

module.exports = {
  target: 'node',
  resolve: {
    alias: aliases,
    extensions: ['', '.js']
  },
  externals: [nodeExternals({
    whitelist: [/\.(?!(?:jsx?|json)$).{1,5}$/i]
  })],
  module: {
    loaders: [
      {
        test: /\.js$/,
        exclude: /(node_modules|bower_components)/,
        loader: 'babel',
        query: { presets: ['es2015', 'react', 'stage-0']}
      },
      {
        test: /\.scss|css$/,
        loader: "css-loader!sass-loader"
      },
      {
        test: /\.woff(2)?(\?v=[0-9]\.[0-9]\.[0-9])?$/,
        loader: "url-loader?limit=10000&mimetype=application/font-woff"
      },
      {
        test: /\.(ttf|eot|svg)(\?v=[0-9]\.[0-9]\.[0-9])?$/,
        loader: "file-loader"
      },
      {
        test: /\.json$/,
        loader: "json-loader"
      }
    ]
  }
}
