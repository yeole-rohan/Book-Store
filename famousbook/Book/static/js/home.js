var $ = jQuery.noConflict();
$(document).ready(
  (function () {
    $(".testimonials-slider-loop").slick({
      infinite: true,
      slidesToShow: 3,
      centerPadding: "0",
      slidesToScroll: -1,
      cssEase: "linear",
      centerMode: true,
      autoplay: false,
      responsive: [
        {
          breakpoint: 899,
          settings: {
            slidesToShow: 2,
            slidesToScroll: 1,
          },
        },
        {
          breakpoint: 676,
          settings: {
            slidesToShow: 1,
            slidesToScroll: 1,
          },
        },
      ],
    });
    $(".featured-author-loop")
      .on("afterChange init", function (event, slick, direction) {
        // console.log('afterChange/init', event, slick, slick.$slides);
        // remove all prev/next
        slick.$slides.removeClass("prevSlide").removeClass("nextSlide");

        // find current slide
        for (var i = 0; i < slick.$slides.length; i++) {
          var $slide = $(slick.$slides[i]);
          if ($slide.hasClass("slick-current")) {
            // update DOM siblings
            $slide.prev().addClass("prevSlide");
            $slide.next().addClass("nextSlide");
            break;
          }
        }
      })
      .on("beforeChange", function (event, slick) {
        // optional, but cleaner maybe
        // remove all prev/next
        slick.$slides.removeClass("prevSlide").removeClass("nextSlide");
      }).slick({
        infinite: true,
        slidesToShow: 5,
        centerPadding: "0",
        slidesToScroll: 3,
        cssEase: "linear",
        centerMode: true,
        autoplay: false,
        responsive: [
          {
            breakpoint: 1025,
            settings: {
              slidesToShow: 3,
              slidesToScroll: 1,
            },
          },
          {
            breakpoint: 899,
            settings: {
              slidesToShow: 2,
              slidesToScroll: 1,
            },
          },
          {
            breakpoint: 676,
            settings: {
              slidesToShow: 1,
              slidesToScroll: 1,
            },
          },
        ],
      });
      $(".featured-book-slider").slick({
        infinite: false,
        slidesToScroll: 1,
        slidesToShow: 3,
        autoplay: true,
        responsive: [
          {
            breakpoint: 1024,
            settings: {
              slidesToShow: 3,
              slidesToScroll: 1,
            },
          },
          {
            breakpoint: 899,
            settings: {
              slidesToShow: 2,
              slidesToScroll: 1,
            },
          },
          {
            breakpoint: 767,
            settings: {
              slidesToShow: 2,
              slidesToScroll: 1,
            },
          },
          {
            breakpoint: 676,
            settings: {
              slidesToShow: 1,
              slidesToScroll: 1,
            },
          },
        ],
      });
      $(".book-categories-slider").slick({
        infinite: false,
        slidesToScroll: 1,
        slidesToShow: 4,
        autoplay: true,
        responsive: [
          {
            breakpoint: 1024,
            settings: {
              slidesToShow: 3,
              slidesToScroll: 1,
            },
          },
          {
            breakpoint: 899,
            settings: {
              slidesToShow: 2,
              slidesToScroll: 1,
            },
          },
          {
            breakpoint: 767,
            settings: {
              slidesToShow: 2,
              slidesToScroll: 1,
            },
          },
          {
            breakpoint: 676,
            settings: {
              slidesToShow: 1,
              slidesToScroll: 1,
            },
          },
        ],
      });
      $(".home-banner-slider").slick({
        infinite: false,
        slidesToScroll: 1,
        slidesToShow: 1,
        autoplay: false,
        dots:true,
        arrows:false,
      });

      $(".bundle-deals-slider").slick({
        infinite: false,
        slidesToScroll: 1,
        slidesToShow: 3,
        autoplay: false,
        variableWidth: true,
        responsive: [
          {
            breakpoint: 1024,
            settings: {
              slidesToShow: 3,
              slidesToScroll: 1,
            },
          },
          {
            breakpoint: 899,
            settings: {
              slidesToShow: 2,
              slidesToScroll: 1,
            },
          },
          {
            breakpoint: 767,
            settings: {
              slidesToShow: 2,
              slidesToScroll: 1,
            },
          },
          {
            breakpoint: 676,
            settings: {
              slidesToShow: 1,
              slidesToScroll: 1,
            },
          },
        ],
      });
  })(jQuery)
);
