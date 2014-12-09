({ 
  baseUrl: '../app',
  wrap: true,
  almond: true,
  optimize: 'none',
  mainConfigFile: '../app/js/main.js',
  out: '../.tmp/app.concatenated.js',
  include: ['js/main'],
  name: 'bower_components/almond/almond'
})

