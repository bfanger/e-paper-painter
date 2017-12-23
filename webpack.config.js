const path = require("path");
const webpack = require("webpack");
const HtmlWebpackPlugin = require("html-webpack-plugin");
const FriendlyErrorsWebpackPlugin = require("friendly-errors-webpack-plugin");
const UglifyJsPlugin = require("uglifyjs-webpack-plugin");

const webpackConfig = {
  entry: path.join(__dirname, "src/bootstrap.js"),
  output: {
    filename: "bundle.js",
    path: path.join(__dirname, "build")
  },
  module: {
    rules: [
      {
        test: /\.vue$/,
        loader: "vue-loader"
      },
      {
        test: /\.js$/,
        loader: "babel-loader",
        include: path.join(__dirname, "src")
      }
    ]
  },
  plugins: [
    new HtmlWebpackPlugin({
      template: path.join(__dirname, "src/index.html")
    })
  ]
};
if (process.argv[1].substr(-8) === "/webpack") {
  // Production build
  webpackConfig.devtool = "source-map";
  webpackConfig.plugins.push(
    new webpack.DefinePlugin({
      "process.env.NODE_ENV": JSON.stringify("production")
    })
  );
  webpackConfig.plugins.push(new UglifyJsPlugin());
} else if (process.argv[1].substr(-19) === "/webpack-dev-server") {
  // Dev build (via webpack-dev-server)
  webpackConfig.devServer = {
    quiet: true,
    proxy: {
      "/api": {
        target: "http://localhost:3000"
      }
    }
  };
  webpackConfig.plugins.push(new FriendlyErrorsWebpackPlugin());
  webpackConfig.devtool = "cheap-eval-source-map";
} else {
  throw new Error("Unexpected invocation: " + process.argv[1]);
}

module.exports = webpackConfig;
