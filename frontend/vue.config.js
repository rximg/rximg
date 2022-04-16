module.exports = {
    devServer: {
      proxy: {
        '^/api': {
          target: 'http://localhost:5000',
          changeOrigin: true,
          ws: true,
          logLevel: 'debug',
          // pathRewrite: { '^/api': '/' },
        },
      },
    },
  }
  