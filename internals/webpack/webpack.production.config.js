const path = require('path');
const webpack = require('webpack');
const MiniCssExtractPlugin = require('mini-css-extract-plugin');
const BundleTracker = require('webpack-bundle-tracker');
const WebpackPwaManifest = require('webpack-pwa-manifest');
const OfflinePlugin = require('offline-plugin');
const { HashedModuleIdsPlugin } = require('webpack');
const TerserPlugin = require('terser-webpack-plugin');
const CompressionPlugin = require('compression-webpack-plugin');

module.exports = require('./webpack.base.config')({
  entry: [path.join(process.cwd(), './resources/js/index.js')],
  mode: 'production',
  output: {
    filename: '[name]-[hash].js',
    path: path.resolve(process.cwd(), './src/core/static/app/'),
    publicPath: '/static/app/',
  },
  optimization: {
    minimize: true,
    minimizer: [
      new TerserPlugin({
        terserOptions: {
          warnings: false,
          compress: {
            comparisons: false,
          },
          parse: {},
          mangle: true,
          output: {
            comments: false,
            ascii_only: true,
          },
        },
        parallel: true,
        cache: true,
        sourceMap: true,
      }),
    ],
    nodeEnv: 'production',
    sideEffects: true,
    concatenateModules: true,
    splitChunks: {
      chunks: 'all',
      minSize: 30000,
      minChunks: 1,
      maxAsyncRequests: 5,
      maxInitialRequests: 3,
      name: true,
    },
  },
  plugins: [
    new MiniCssExtractPlugin({
      // Options similar to the same options in webpackOptions.output
      // both options are optional
      filename: 'app.[hash].css',
      chunkFilename: '[id].[hash].css',
    }),
    new OfflinePlugin({
      relativePaths: false,
      publicPath: '/',
      appShell: '/',

      // No need to cache .htaccess. See http://mxs.is/googmp,
      // this is applied before any match in `caches` section
      excludes: [path.resolve(process.cwd(), './resources/.htaccess')],

      caches: {
        main: [':rest:'],

        // All chunks marked as `additional`, loaded after main section
        // and do not prevent SW to install. Change to `optional` if
        // do not want them to be preloaded at all (cached only when first loaded)
        additional: ['*.chunk.js'],
      },

      // Removes warning for about `additional` section usage
      safeToUseOptionalCaches: true,
    }),
    new CompressionPlugin({
      algorithm: 'gzip',
      test: /\.js$|\.css$|\.html$/,
      threshold: 10240,
      minRatio: 0.8,
    }),
    new WebpackPwaManifest({
      name: 'YOYO Weather API',
      short_name: 'YOYO',
      description: 'yoyo-weather-api Frontend module',
      background_color: '#fafafa',
      theme_color: '#2472b1',
      inject: true,
      ios: true,
      // scope: "/",
      icons: [
        {
          src: path.resolve(process.cwd(), './resources/images/Favicon.png'),
          sizes: [72, 96, 128, 144, 192, 384, 512],
        },
        {
          src: path.resolve(process.cwd(), './resources/images/Favicon.png'),
          sizes: [120, 152, 167, 180],
          ios: true,
        },
      ],
    }),
    new HashedModuleIdsPlugin({
      hashFunction: 'sha256',
      hashDigest: 'hex',
      hashDigestLength: 20,
    }),
    new BundleTracker({
      path: path.resolve(process.cwd()),
      filename: './config/webpack-stats-production.json',
    }),
  ],

  performance: {
    assetFilter: assetFilename =>
      !/(\.map$)|(^(main\.|favicon\.))/.test(assetFilename),
  },
});
