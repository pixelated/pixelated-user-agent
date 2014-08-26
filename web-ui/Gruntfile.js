/*
 * Copyright (c) 2014 ThoughtWorks, Inc.
 *
 * Pixelated is free software: you can redistribute it and/or modify
 * it under the terms of the GNU Affero General Public License as published by
 * the Free Software Foundation, either version 3 of the License, or
 * (at your option) any later version.
 *
 * Pixelated is distributed in the hope that it will be useful,
 * but WITHOUT ANY WARRANTY; without even the implied warranty of
 * MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
 * GNU Affero General Public License for more details.
 *
 * You should have received a copy of the GNU Affero General Public License
 * along with Pixelated. If not, see <http://www.gnu.org/licenses/>.
 */
'use strict';

// # Globbing
// for performance reasons we're only matching one level down:
// 'test/spec/{,*/}*.js'
// use this if you want to recursively match all subfolders:
// 'test/spec/**/*.js'

module.exports = function (grunt) {
  var exec = require('child_process').exec;

 // Load grunt tasks automatically
  require('load-grunt-tasks')(grunt);

  // Time how long tasks take. Can help when optimizing build times
  require('time-grunt')(grunt);

  // Define the configuration for all the tasks
  grunt.initConfig({
    compress: {
      main: {
        options: {
          archive: 'archive.zip'
        },
        files: [
          {src: ['dist/**/*']} // includes files in path
        ]
      }
    },

    // Project settings
    yeoman: {
      // configurable paths
      app: require('./bower.json').appPath || 'app',
      dist: 'dist'
    },

    // Watches files for changes and runs tasks based on the changed files
    watch: {
      js: {
        files: ['{.tmp,<%= yeoman.app %>}/js/{,*/}*.js'],
        tasks: ['newer:jshint:all', 'update-control-tower']
      },
      jsTest: {
        files: ['test/spec/{,*/}*.js'],
        tasks: ['newer:jshint:test', 'karma']
      },
      sass: {
        files: ['<%= yeoman.app %>/scss/{,*/}*.scss'],
        tasks: ['compass:dev']
      },
      html: {
        files: ['<%= yeoman.app %>/index.html'],
        livereload: true
      },
      templates: {
        files: ['<%= yeoman.app %>/templates/**/*.hbs'],
        tasks: ['handlebars:dev']
      },
      gruntfile: {
        files: ['Gruntfile.js']
      }
    },

    compass: {
      dist: {
        options: {
          sassDir: '<%= yeoman.app %>/scss',
          cssDir: '<%= yeoman.dist %>/css',
          environment: 'production'
        }
      },
      dev: {
        options: {
          sassDir: '<%= yeoman.app %>/scss',
          cssDir: 'app/css'
        }
      }
    },

    // The actual grunt server settings
    connect: {
      options: {
        port: 9000,
        // Change this from '0.0.0.0' to 'localhost' to limit access from outside.
        hostname: '0.0.0.0',
        livereload: true
      },
      test: {
        options: {
          port: 9001,
          base: [
            '.tmp',
            'test',
            '<%= yeoman.app %>'
          ]
        }
      },
      dist: {
        options: {
          base: '<%= yeoman.dist %>'
        }
      }
    },

    // Make sure code styles are up to par and there are no obvious mistakes
    jshint: {
      options: {
        jshintrc: '.jshintrc',
        reporter: require('jshint-stylish')
      },
      all: [
        'Gruntfile.js',
        '<%= yeoman.app %>/scripts/{,*/}*.js'
      ],
      test: {
        options: {
          jshintrc: '.jshintrc'
        },
        src: ['test/spec/{,*/}*.js']
      }
    },

    // Empties folders to start fresh
    clean: {
      dist: {
        files: [{
          dot: true,
          src: [
            '.tmp',
            '<%= yeoman.dist %>/*',
          ]
        }]
      },
      server: ['.tmp', '<%= yeoman.app %>/js/generated']
    },

    uglify: {
      dist: {
        files: [{
          expand: true,
          cwd: '.tmp',
          src: 'app.min.js',
          dest: 'dist'
        }]
      }
    },

    cssmin: {
      minify: {
        expand: true,
        cwd: '<%= yeoman.app %>/css/',
        src: ['*.css', '!*.min.css'],
        dest: '<%= yeoman.dist %>/css/'
      }
    },

    // The following *-min tasks produce minified files in the dist folder
    imagemin: {
      dist: {
        files: [{
          expand: true,
          cwd: '<%= yeoman.app %>/images',
          src: '{,*/}*.{png,jpg,jpeg,gif}',
          dest: '<%= yeoman.dist %>/images'
        }]
      }
    },

    svgmin: {
      dist: {
        files: [{
          expand: true,
          cwd: '<%= yeoman.app %>/images',
          src: '{,*/}*.svg',
          dest: '<%= yeoman.dist %>/images'
        }]
      }
    },

    htmlmin: {
      dist: {
        options: {
          // Optional configurations that you can uncomment to use
          // removeCommentsFromCDATA: true,
          // collapseBooleanAttributes: true,
          // removeAttributeQuotes: true,
          // removeRedundantAttributes: true,
          // useShortDoctype: true,
          // removeEmptyAttributes: true,
          // removeOptionalTags: true*/
        },
        files: [{
          expand: true,
          cwd: '<%= yeoman.app %>',
          src: ['*.html', 'templates/*.html'],
          dest: '<%= yeoman.dist %>'
        }]
      }
    },

    // Allow the use of non-minsafe AngularJS files. Automatically makes it
    // minsafe compatible so Uglify does not destroy the ng references
    // Replace Google CDN references
    cdnify: {
      dist: {
        html: ['<%= yeoman.dist %>/*.html']
      }
    },

    // Copies remaining files to places other tasks can use
    copy: {
      dist: {
        files: [{
          expand: true,
          dot: true,
          cwd: '<%= yeoman.app %>',
          dest: '<%= yeoman.dist %>',
          src: [
            '*.{ico,png,txt}',
            '.htaccess',
            'images/{,*/}*.{webp}',
            'fonts/*',
            'templates/*',
            'locales/**/*',
            'bower_components/font-awesome/css/font-awesome.min.css',
            'bower_components/font-awesome/fonts/*'
          ]
        }, {
          expand: true,
          cwd: '.tmp/images',
          dest: '<%= yeoman.dist %>/images',
          src: [
            'generated/*'
          ]
        }]
      },
      styles: {
        expand: true,
        cwd: '<%= yeoman.app %>/styles',
        dest: '.tmp/css/',
        src: '{,*/}*.css'
      }
    },

    // Run some tasks in parallel to speed up the build process
    concurrent: {
      server: [
        'copy:styles'
      ],
      test: [
        'copy:styles'
      ],
      dist: [
        'copy:styles',
        'imagemin',
        'svgmin',
        'htmlmin'
      ]
    },
    requirejs: {
      compile: {
        options: {
          baseUrl: 'app',
          wrap: true,
          almond: true,
          optimize: 'none',
          mainConfigFile: 'app/js/main.js',
          out: '.tmp/app.concatenated.js',
          include: ['js/main'],
          name: 'bower_components/almond/almond'

        }
      }
    },
    concat: {
      options: {
        separator: ';',
      },
      dist: {
        src: [
          'app/bower_components/modernizr/modernizr.js',
          'app/bower_components/lodash/dist/lodash.js',
          'app/bower_components/jquery/dist/jquery.js',
          'app/js/lib/highlightRegex.js',
          'app/bower_components/handlebars/handlebars.min.js',
          'app/bower_components/typeahead.js/dist/typeahead.bundle.min.js',
          'app/bower_components/foundation/js/foundation.js',
          'app/bower_components/foundation/js/foundation/foundation.reveal.js',
          'app/bower_components/foundation/js/foundation/foundation.offcanvas.js',
          '.tmp/app.concatenated.js',
        ],
        dest: '.tmp/app.min.js',
      },
    },
    useminPrepare: {
      html: 'dist/index.html',
      options: {
        dest: 'dist'
      }
    },
    usemin: {
      html: 'dist/index.html'
    },
    'regex-replace': {
      dist: {
        src: ['dist/index.html'],
        actions: [
          {
            name: 'remove-requirejs-from-index',
            search: 'remove-in-build.*end-remove-in-build',
            replace: function(match){
              return '';
            },
            flags: 'g'
          }
        ]
      }
    },
    handlebars: {
      dist: {
        options: {
          namespace: 'Pixelated'
        },
        files: {
          '<%= yeoman.dist %>/js/generated/hbs/templates.js': '<%= yeoman.app %>/templates/**/*.hbs'
        }
      },
      dev: {
        options: {
          namespace: 'Pixelated'
        },
        files: {
          '<%= yeoman.app %>/js/generated/hbs/templates.js': '<%= yeoman.app %>/templates/**/*.hbs'
        }
      }
    },

    // Test settings
    karma: {
      options: {
        configFile: 'karma.conf.js'
      },

      ci: {
        singleRun: true,
        autoWatch: false,
        colors: false,
        reporters: ['junit']
      },

      single: {
        singleRun: true,
        autoWatch: false
      },

      dev: {
        singleRun: false,
        browsers: ['PhantomJS']
      },
      debug: {
        singleRun: false,
        browsers: ['Chrome']
      }

    }

  });

  grunt.loadNpmTasks('grunt-contrib-requirejs');
  grunt.loadNpmTasks('grunt-contrib-concat');

  grunt.registerTask('build', function (target) {
    if (target === 'dist') {
      return grunt.task.run(['package', 'dist:keepalive']);
    }

    grunt.task.run([
      'clean:server',
      'compass:dev',
      'handlebars:dev',
      'concurrent:server',
      'update-control-tower'
    ]);
  });

  /*
  grunt.registerTask('watch', function (target) {
    grunt.task.run([
      'build',
      'watch'
    ]);
  });
  */

  grunt.registerTask('test-watch', [
    'clean:server',
    'handlebars:dev',
    'connect:test',
    'karma:dev'
  ]);

  grunt.registerTask('debug', [
    'clean:server',
    'handlebars:dev',
    'connect:test',
    'karma:debug'
  ]);

  grunt.registerTask('test-ci', [
    'clean:server',
    'stopbrowsers',
    'handlebars:dev',
    'concurrent:test',
    'connect:test',
    'karma:ci'
  ]);

  grunt.registerTask('test', [
    'clean:server',
    'handlebars:dev',
    'connect:test',
    'karma:single'
  ]);

  grunt.registerTask('package', [
    'clean:dist',
    'useminPrepare',
    'compass:dist',
    'handlebars:dev',
    'concurrent:dist',
    'copy:dist',
    'cdnify',
    'cssmin',
    'requirejs',
    'concat:dist',
    'uglify',
    'usemin',
    'regex-replace:dist',
    'compress'
  ]);

  grunt.registerTask('default', [
    'newer:jshint',
    'test',
    'package'
  ]);

  grunt.registerTask('stopbrowsers', function () {
    ['phantom', 'firefox'].forEach(function (browser) {
      console.log('killing all ' + browser + ' instances');
      exec('pgrep -f "' + browser + '" | xargs kill');
      console.log('... done');
    });
  });

  grunt.registerTask('update-control-tower', function () {
    exec('bash -c "flight-control-tower control-tower.yml && mv control_tower.html .tmp/"');
  });
};
