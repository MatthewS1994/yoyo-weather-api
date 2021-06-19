const path = require('path');
const webpack = require('webpack');
const MiniCssExtractPlugin = require('mini-css-extract-plugin');
const CircularDependencyPlugin = require('circular-dependency-plugin');
const BundleTracker = require('webpack-bundle-tracker');

const PORT = 3000;

module.exports = require('./webpack.base.config')({
  entry: [
    'webpack/hot/dev-server',
    path.join(process.cwd(), './resources/js/index.js'),
  ],
  mode: 'development',
  output: {
    filename: '[name].js',
    path: path.resolve(process.cwd(), './src/core/static/app/'),
    publicPath: `http://localhost:${PORT}/static/app/`,
  },
  devServer: {
    contentBase: path.resolve(process.cwd(), './resources'),
    hot: true,
    port: PORT,
    headers: {
      'Access-Control-Allow-Origin': '*',
    },
    proxy: {
      '!*': {
        target: 'http://localhost:8000', // points to django dev server
        changeOrigin: true,
      },
    },
  },
  optimization: {
    splitChunks: {
      chunks: 'all',
    },
  },
  devtool: 'source-map',
  performance: {
    hints: false,
  },
  plugins: [
    new webpack.HotModuleReplacementPlugin(), // Tell webpack we want hot reloading
    new webpack.NoEmitOnErrorsPlugin(),
    new MiniCssExtractPlugin({
      // Options similar to the same options in webpackOptions.output
      // both options are optional
      filename: 'app.css',
      chunkFilename: '[id].css',
    }),
    new CircularDependencyPlugin({
      exclude: /a\.js|node_modules/, // exclude node_modules
      failOnError: false, // show a warning when there is a circular dependency
    }),
    new BundleTracker({
      path: path.resolve(process.cwd()),
      filename: './config/webpack-stats.json',
    }),
  ],
});
