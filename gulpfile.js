// This gulp support is experimental, and any given web project may have
// it's own gulp setup that should be used before using this setup.

// The gulp setup here may not even work for some web projects.

// To configure, copy `example.gulp-config.yml` to `example.gulp-config.yml`, and edit
// that file as required.

// Include gulp.
var gulp = require('gulp');
var browserSync = require('browser-sync').create();

// Include plugins.
var sass = require('gulp-sass');
var imagemin = require('gulp-imagemin');
var pngcrush = require('imagemin-pngcrush');
var shell = require('gulp-shell');
var plumber = require('gulp-plumber');
var notify = require('gulp-notify');
var autoprefix = require('gulp-autoprefixer');
var glob = require('gulp-sass-glob');
var uglify = require('gulp-uglify');
var concat = require('gulp-concat');
var rename = require('gulp-rename');
var sourcemaps = require('gulp-sourcemaps');
var scssLint = require('gulp-scss-lint');
var jshint = require('gulp-jshint');

// Load config
var YAML = require('yamljs');
var config = YAML.load('gulp-config.yml');

// CSS.
gulp.task('css', function() {
  return gulp.src(config.themeDir + '/' + config.css.src)
    .pipe(glob())
    .pipe(plumber({
      errorHandler: function (error) {
        notify.onError({
          title:    "Gulp",
          subtitle: "Failure!",
          message:  "Error: <%= error.message %>",
          sound:    "Beep"
        }) (error);
        this.emit('end');
      }}))
    .pipe(sourcemaps.init())
    .pipe(sass({
      outputStyle: config.css.outputStyle,
      errLogToConsole: true,
      includePaths: config.css.includePaths
    }))
    .pipe(autoprefix('last 2 versions', '> 1%', 'ie 9', 'ie 10'))
    .pipe(sourcemaps.write())
    .pipe(gulp.dest(config.themeDir + '/' + config.css.dest))
    .pipe(browserSync.reload({ stream: true, match: '**/*.css' }));
});

// Compress images.
gulp.task('images', function () {
  return gulp.src(config.themeDir + '/' + config.images.src)
    .pipe(imagemin({
      progressive: true,
      svgoPlugins: [{ removeViewBox: false }],
      use: [pngcrush()]
    }))
    .pipe(gulp.dest(config.themeDir + '/' + config.images.dest));
});

// Fonts.
gulp.task('fonts', function() {
  return gulp.src(config.fonts.src)
    .pipe(gulp.dest(config.themeDir + '/' + config.fonts.dest));
});

// Watch task.
gulp.task('watch', function() {
  gulp.watch(config.themeDir + '/' + config.css.src, ['css']);
  gulp.watch(config.themeDir + '/' + config.images.src, ['images']);
});

// Static Server + Watch
gulp.task('serve', ['css', 'fonts', 'watch'], function() {
  browserSync.init({
    proxy: config.browserSyncProxy
  });
});

// Run drush to clear the theme registry.
gulp.task('drush', shell.task([
  'drush ' + config.drushAlias + ' cache-clear theme-registry'
]));

// SCSS Linting.
gulp.task('scss-lint', function() {
  return gulp.src([config.themeDir + '/' + config.css.src])
    .pipe(scssLint())
    .pipe(scssLint.format())
    .pipe(scssLint.failOnError());
});

// JS Linting.
gulp.task('js-lint', function() {
  return gulp.src(config.themeDir + '/' + config.js.src)
    .pipe(jshint())
    .pipe(jshint.reporter('default'));
});

// Default Task
gulp.task('default', ['serve']);
