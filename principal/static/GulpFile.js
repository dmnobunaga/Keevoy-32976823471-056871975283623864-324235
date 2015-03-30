'use strict';

var gulp = require('gulp'),
    watch = require('gulp-watch'),
    concat = require('gulp-concat'),
    prefixer = require('gulp-autoprefixer'),
    order = require('gulp-order'),
    uglify = require('gulp-uglify'),
    cssminify = require('gulp-minify-css'),
    less = require('gulp-less'),
    sourcemaps = require('gulp-sourcemaps'),
    rigger = require('gulp-rigger'),
    cssimport = require('gulp-cssimport'),
    cssbase64 = require('gulp-css-base64'),
    imagemin = require('gulp-imagemin'),
    pngquant = require('imagemin-pngquant'),
    rimraf = require('rimraf'),
    browserSync = require('browser-sync'),
    opn = require('opn');

var path = {
    build: { //Тут мы укажем куда складывать готовые после сборки файлы
        js: 'front-end/build/js/',
        css: 'front-end/build/css/',
        img: 'front-end/build/img/',
        fonts: 'front-end/build/fonts/'
    },
    src: { //Пути откуда брать исходники
        js: 'front-end/js/**/*.js',// В стилях и скриптах нам понадобятся только main файлы
        style: 'front-end/css/**/*.css',
        img: 'front-end/img/**/*.*', // Синтаксис img/**/*.* означает - взять все файлы всех расширений из папки и из вложенных каталогов
        fonts: 'front-end/fonts/**/*.*'
    },
    watch: { //Тут мы укажем, за изменением каких файлов мы хотим наблюдать
        js: 'front-end/js/**/*.js',
        style: 'front-end/css/**/*.css',
        img: 'front-end/img/**/*.*',
        fonts: 'front-end/fonts/**/*.*'
    },
    clean: './build'
};

var config = {
    proxy: "http://127.0.0.1:8000/",
    files: [path.build.css + "*.css", path.build.js + "*.js"]
};
var reload = browserSync(config).reload;

gulp.task('browser-sync', function () {
    browserSync(config);

});
gulp.task('style:build', function () {
    gulp.src(path.src.style) //Выберем наш style.less
        .pipe(prefixer()) //Добавим вендорные префиксы
        .pipe(cssimport()) //
        //.pipe(cssbase64()) // Img to Cssbase64
        .pipe(cssminify({keepSpecialComments: 0})) //Сожмем
        .pipe(gulp.dest(path.build.css)) //И в build
        .pipe(reload({stream: true}));

});
gulp.task('image:build', function () {
    gulp.src(path.src.img) //Выберем наши картинки
        .pipe(imagemin({ //Сожмем их
            progressive: true,
            use: [pngquant()],
            interlaced: true
        }))
        .pipe(gulp.dest(path.build.img)) //И бросим в build;
        .pipe(reload({stream: true}));
});
gulp.task('fonts:build', function () {
    gulp.src(path.src.fonts)
        .pipe(gulp.dest(path.build.fonts))
});
gulp.task('js:build', function () {
    gulp.src(path.src.js) //Выберем наши js
        .pipe(uglify()) //Compress
        .pipe(order([
            'front-end/js/plugins/jquery/jquery.min.js',
            'front-end/js/plugins/bootstrap/bootstrap.min.js',
            'front-end/js/plugins/mixitup/jquery.mixitup.js',
            'front-end/js/plugins/appear/jquery.appear.js',
            'front-end/js/plugins/revolution-slider/jquery.themepunch.tools.min.js',
            'front-end/js/plugins/revolution-slider/jquery.themepunch.revolution.min.js',
            'front-end/js/actions.js',
            'front-end/js/slider.js',
            'front-end/js/main.js'
        ], {base: './'})) // Order
        .pipe(concat("all.js")) //Concat
        .pipe(gulp.dest(path.build.js)) //И в build
        .pipe(reload({stream: true}));
});

gulp.task('default', ['browser-sync'], function () {
    gulp.watch("../../templates/front-end/*.html").on('change', reload);//Watch templates

    gulp.watch(path.src.style, ['style:build'], function () { //Watch style
        //reload();
    });

    gulp.watch(path.src.js, ['js:build'], function () { // Watch js
        //reload();
    });
    'use strict';

    var gulp = require('gulp'),
        watch = require('gulp-watch'),
        concat = require('gulp-concat'),
        prefixer = require('gulp-autoprefixer'),
        order = require('gulp-order'),
        uglify = require('gulp-uglify'),
        cssminify = require('gulp-minify-css'),
        less = require('gulp-less'),
        sourcemaps = require('gulp-sourcemaps'),
        rigger = require('gulp-rigger'),
        cssimport = require('gulp-cssimport'),
        cssbase64 = require('gulp-css-base64'),
        imagemin = require('gulp-imagemin'),
        pngquant = require('imagemin-pngquant'),
        rimraf = require('rimraf'),
        connect = require('gulp-connect'),
        opn = require('opn');

    var path = {
        build: { //Тут мы укажем куда складывать готовые после сборки файлы
            js: 'front-end/build/js/',
            css: 'front-end/build/css/',
            img: 'front-end/build/img/',
            fonts: 'front-end/build/fonts/'
        },
        src: { //Пути откуда брать исходники
            js: 'front-end/js/**/*.js',// В стилях и скриптах нам понадобятся только main файлы
            style: 'front-end/css/**/*.css',
            img: 'front-end/img/**/*.*', // Синтаксис img/**/*.* означает - взять все файлы всех расширений из папки и из вложенных каталогов
            fonts: 'front-end/fonts/**/*.*'
        },
        watch: { //Тут мы укажем, за изменением каких файлов мы хотим наблюдать
            js: 'front-end/js/**/*.js',
            style: 'front-end/css/**/*.css',
            img: 'front-end/img/**/*.*',
            fonts: 'front-end/fonts/**/*.*'
        },
        clean: './build'
    };

    gulp.task('style:build', function () {
        gulp.src(path.src.style) //Выберем наш style.less
            .pipe(prefixer()) //Добавим вендорные префиксы
            .pipe(cssimport()) //
            //.pipe(cssbase64()) // Img to Cssbase64
            .pipe(cssminify({keepSpecialComments: 0})) //Сожмем
            .pipe(gulp.dest(path.build.css)) //И в build
            .pipe(connect.reload());
    });

    gulp.task('image:build', function () {
        gulp.src(path.src.img) //Выберем наши картинки
            .pipe(imagemin({ //Сожмем их
                progressive: true,
                use: [pngquant()],
                interlaced: true
            }))
            .pipe(gulp.dest(path.build.img)) //И бросим в build
            .pipe(connect.reload());
    });
    gulp.task('fonts:build', function () {
        gulp.src(path.src.fonts)
            .pipe(gulp.dest(path.build.fonts))
    });
    gulp.task('js:build', function () {
        gulp.src(path.src.js) //Выберем наши js
            .pipe(uglify()) //Compress
            .pipe(order([
                'front-end/js/plugins/jquery/jquery.min.js',
                'front-end/js/plugins/bootstrap/bootstrap.min.js',
                'front-end/js/plugins/mixitup/jquery.mixitup.js',
                'front-end/js/plugins/appear/jquery.appear.js',
                'front-end/js/plugins/revolution-slider/jquery.themepunch.tools.min.js',
                'front-end/js/plugins/revolution-slider/jquery.themepunch.revolution.min.js',
                'front-end/js/actions.js',
                'front-end/js/slider.js'
            ], {base: './'})) // Order
            .pipe(concat("all.js")) //Concat
            .pipe(gulp.dest(path.build.js)) //И в build
            .pipe(connect.reload());
    });
});