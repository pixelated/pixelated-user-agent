var Imagemin = require('imagemin');

var imagemin = new Imagemin()
  .src('app/images/*.{gif,jpg,png,svg}')
  .dest('dist/images')
  .use(Imagemin.jpegtran({ progressive: true }));

imagemin.run(function (err, files) {
  if (err) {
  throw err;
  }

  console.log(files[0]);
});
