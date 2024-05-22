const { override, addWebpackModuleRule } = require("customize-cra");

console.log("Applying custom webpack configuration...");

module.exports = override(
  addWebpackModuleRule({
    test: /\.svg$/,
    use: ["@svgr/webpack"],
  })
);
