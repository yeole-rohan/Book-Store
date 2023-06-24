var $ = jQuery.noConflict();
$(document).ready((function () {
    $(".history-book-slider").slick({
        infinite: false,
        slidesToScroll: 1,
        slidesToShow: 4,
        autoplay: true,
        responsive: [
          {
            breakpoint: 1300,
            settings: {
              slidesToShow: 3,
              slidesToScroll: 1,
            },
          },
          {
            breakpoint: 1024,
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
              arrows:false,
            },
          },
          {
            breakpoint: 599,
            settings: {
              slidesToShow: 1,
              slidesToScroll: 1,
              arrows:false,
            },
          },
        ],
      });
})(jQuery)
);
