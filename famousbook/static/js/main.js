var $ = jQuery.noConflict();
$(document).ready((function () {
  /**
   * Attaches a click event listener to the ".add-to-cart" element. When clicked, an AJAX request is sent to the server to add the book to the cart.
   * @param {object} params - The event object.
   * @returns None
   */
  $(document).on("click", ".add-to-cart", function (params) {
    params.preventDefault();
    var currentElement = $(this)
    var parent = this.parentElement
    $.ajax({
      url: currentElement.attr("href"),
      data: {
        book_id: currentElement.attr("data-book-id"),
        csrfmiddlewaretoken: $("input[name=csrfmiddlewaretoken]").val(),
      },
      type: "POST",
      dataType: "json",
      success: function (res, status) {
        if (res.success) {
          document.querySelector(".cart-count").textContent = res.cartCount
          parent.innerHTML = '<a href="/cart/" class="d-inline-block weight-500 font-24" tabindex="-1">Go to Cart</a>'
          var aMessage = '<div class="alert alert-success alert-dismissible fade show" role="alert">'+
          res.message +'<button type="button" class="btn-close" data-bs-dismiss="alert" aria-label="Close"></button>'
          $(".messages").append(aMessage);
        }else{
          var aMessage = '<div class="alert alert-danger alert-dismissible fade show" role="alert">'+
            res.message +'<button type="button" class="btn-close" data-bs-dismiss="alert" aria-label="Close"></button>'
            $(".messages").append(aMessage);
        }
      },
      error: function (res) {
        var aMessage = '<div class="alert alert-danger alert-dismissible fade show" role="alert">Something went wrong, while adding to cart.<button type="button" class="btn-close" data-bs-dismiss="alert" aria-label="Close"></button>'
        $(".messages").append(aMessage);
      },
    });
  });

  /**
   * Adds a book to the user's wishlist when the "add-to-wishlist" button is clicked.
   * @param {object} params - The event object.
   * @returns None
   */
  $(document).on("click", ".add-to-wishlist-card", function (params) {
    params.preventDefault();
    var currentElement = $(this)
    var parent = this.parentElement
    $.ajax({
      url: currentElement.attr("href"),
      data: {
        bookId: currentElement.attr("data-book-id"),
        csrfmiddlewaretoken: $("input[name=csrfmiddlewaretoken]").val(),
      },
      type: "POST",
      dataType: "json",
      success: function (res, status) {
        if (res.success) {
          currentElement.remove()
          var div = document.createElement("div")
          div.innerHTML = '<img src="/static/img/favorite.svg">'
          div.className = "add-to-wishlist-card-none"
          parent.prepend(div)
          console.log( res.wishCount);
          
          document.querySelector(".wish-count").textContent = res.wishCount
          var aMessage = '<div class="alert alert-success alert-dismissible fade show" role="alert">'+
          res.message +'<button type="button" class="btn-close" data-bs-dismiss="alert" aria-label="Close"></button>'
          $(".messages").append(aMessage);
        }else{
          var aMessage = '<div class="alert alert-danger alert-dismissible fade show" role="alert">'+
            res.message +'<button type="button" class="btn-close" data-bs-dismiss="alert" aria-label="Close"></button>'
            $(".messages").append(aMessage);
        }
      },
      error: function (res) {
        var aMessage = '<div class="alert alert-danger alert-dismissible fade show" role="alert">Make Sure you logged in.<button type="button" class="btn-close" data-bs-dismiss="alert" aria-label="Close"></button>'
        $(".messages").append(aMessage);
      },
    });
  });

  /**
   * Attaches an event listener to the document that listens for input events on elements with the class "search-box".
   * When an input event is detected, an AJAX request is sent to the server to retrieve search suggestions based on the input value.
   * If the request is successful, the search suggestions are displayed in an HTML element with the class "search-suggestion".
   * @param {object} params - additional parameters to pass to the event listener (not used in this function)
   * @returns None
   */
  $(document).on("input", ".search-box", function (params) {
    // var getLastString = this.value.split(" ")
    // console.log(getLastString);
    $.ajax({
      url: $(this).attr("data-href"),
      data: {
        // keyword: getLastString[getLastString.length - 1].trim(),
        keyword: this.value,
        csrfmiddlewaretoken: $("input[name=csrfmiddlewaretoken]").val(),
      },
      type: "POST",
      dataType: "json",
      success: function (res, status) {
        if (res["status"] == "ok") {
          var result = "";
          if (res.suggestions.length > 0) {
            for (let i = 0; i < res.suggestions.length; i++) {
              const element = res.suggestions[i];
              result +=
                "<a href='/details/" + element[1] + "/' class='single-suggestion'>" + element[0] + "</a>";
            }
            document.querySelector(".search-suggestion").style.border =
              "1px solid #dadee3";
            document.querySelector(".search-suggestion").innerHTML = result;
          } else {
            document.querySelector(".search-suggestion").innerHTML = '';
            document.querySelector(".search-suggestion").style.border = "none"
          }
        }
      },
      error: function (res) {
        console.error(res.status);
      },
    });
  });
  $(document).on("input", ".mobile-search-box-form .search-box", function (params) {
    // var getLastString = this.value.split(" ")
    // console.log(getLastString);
    $.ajax({
      url: $(this).attr("data-href"),
      data: {
        // keyword: getLastString[getLastString.length - 1].trim(),
        keyword: this.value,
        csrfmiddlewaretoken: $("input[name=csrfmiddlewaretoken]").val(),
      },
      type: "POST",
      dataType: "json",
      success: function (res, status) {
        if (res["status"] == "ok") {
          var result = "";
          if (res.suggestions.length > 0) {
            for (let i = 0; i < res.suggestions.length; i++) {
              const element = res.suggestions[i];
              result +=
                "<a href='/details/" + element[1] + "/' class='single-suggestion'>" + element[0] + "</a>";
            }
            document.querySelector(".mobile-search-suggestion").style.border =
              "1px solid #dadee3";
            document.querySelector(".mobile-search-suggestion").innerHTML = result;
          } else {
            document.querySelector(".mobile-search-suggestion").innerHTML = '';
            document.querySelector(".mobile-search-suggestion").style.border = "none"
          }
        }
      },
      error: function (res) {
        console.error(res.status);
      },
    });
  });
  $(document).on("click", "#hamburger",  function(params){
    params.preventDefault()
    $(".mobile-lists").toggle()
  })
  var cachedWidth = $(window).width();
    window.onresize = function () {
      var newWidth = $(window).width();
      if (newWidth != cachedWidth) {
        if (window.innerWidth <= 1024) {
          $(".mobile-lists").css("display", "none");
        }
        cachedWidth = newWidth;
      }
    };
})(jQuery)
);
