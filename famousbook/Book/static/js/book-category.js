var $ = jQuery.noConflict();
$(document).ready((function () {
  var categoryList = []
  var binding = []
  var language = []
  var price = []
  discountPrice = []
  $(document).on("click", "input[type='checkbox']", function (event) {
    console.log(event.target.name, event.target.value, event.target.checked);
    if (event.target.name.includes("secondary")) {
      if (event.target.checked) {
        categoryList.push(event.target.value)

      } else {
        const index = categoryList.indexOf(event.target.value)
        if (index > -1) {
          categoryList.splice(index, 1)
        }
      }
    } else if (event.target.name.includes("binding")) {
      if (event.target.checked) {
        binding.push(event.target.value)
      } else {
        const index = binding.indexOf(event.target.value)
        if (index > -1) {
          binding.splice(index, 1)
        }
      }
    } else if (event.target.name.includes("language")) {
      if (event.target.checked) {
        language.push(event.target.value)
      } else {
        const index = language.indexOf(event.target.value)
        if (index > -1) {
          language.splice(index, 1)
        }
      }
    } else if (event.target.name.includes("price")) {
      if (event.target.checked) {
        price.push(event.target.value)
      } else {
        const index = price.indexOf(event.target.value)
        if (index > -1) {
          price.splice(index, 1)
        }
      }
    } else if (event.target.name.includes("flexCheckChecked")) {
      if (event.target.checked) {
        discountPrice.push(event.target.value)
      } else {
        const index = discountPrice.indexOf(event.target.value)
        if (index > -1) {
          discountPrice.splice(index, 1)
        }
      }
    }
    console.log(categoryList, binding, price);
    $.ajax({
      url: "/search/advance/",
      data: {
        "categoryList": categoryList,
        "binding": binding,
        "language": language,
        "price": price,
        "discountPrice": discountPrice,
        "category": document.getElementById("category").value,
        csrfmiddlewaretoken: $("input[name=csrfmiddlewaretoken]").val(),
      },
      type: "POST",
      dataType: "json",
      beforeSend: function () {
        // document.querySelector(".outer-rim").classList.remove("hide");
      },
      success: function (res, status) {
        // console.log(res, status);
        if (res.success) {
          var wishList = res["wishList"];
          var userCart = res["userCart"];
          var result = '<div class="row">'
          var books = res["bookList"]
          // console.log(books,);
          // Iterate through the received data and append it to the .row class
          for (let i = 0; i < books.length; i++) {
            const book = books[i];
            // console.log(book, "--------------");
            result += '<div class="col-lg-4 col-md-6 col-sm-6">'
            result += '<div class="book-card position-relative">'
            console.log(result, "initial");
            if (wishList.includes(book.id)) {
              result += '<div class="add-to-wishlist-card-none"><img src="/static/img/favorite.svg"></div>'
            } else {
              result += '<a class="add-to-wishlist-card" data-book-id="' + book.id + '" href="/wishlist/add/"><svg width="25" height="23" viewBox="0 0 25 23" fill="none" xmlns="http://www.w3.org/2000/svg"><path d="M12.5 22.9375L10.6875 21.3125C8.58333 19.4167 6.84375 17.7812 5.46875 16.4062C4.09375 15.0312 3 13.7969 2.1875 12.7031C1.375 11.6094 0.807292 10.6042 0.484375 9.6875C0.161458 8.77083 0 7.83333 0 6.875C0 4.91667 0.65625 3.28125 1.96875 1.96875C3.28125 0.65625 4.91667 0 6.875 0C7.95833 0 8.98958 0.229167 9.96875 0.6875C10.9479 1.14583 11.7917 1.79167 12.5 2.625C13.2083 1.79167 14.0521 1.14583 15.0313 0.6875C16.0104 0.229167 17.0417 0 18.125 0C20.0833 0 21.7188 0.65625 23.0313 1.96875C24.3438 3.28125 25 4.91667 25 6.875C25 7.83333 24.8385 8.77083 24.5156 9.6875C24.1927 10.6042 23.625 11.6094 22.8125 12.7031C22 13.7969 20.9062 15.0312 19.5312 16.4062C18.1562 17.7812 16.4167 19.4167 14.3125 21.3125L12.5 22.9375ZM12.5 19.5625C14.5 17.7708 16.1458 16.2344 17.4375 14.9531C18.7292 13.6719 19.75 12.5573 20.5 11.6094C21.25 10.6615 21.7708 9.81771 22.0625 9.07812C22.3542 8.33854 22.5 7.60417 22.5 6.875C22.5 5.625 22.0833 4.58333 21.25 3.75C20.4167 2.91667 19.375 2.5 18.125 2.5C17.1458 2.5 16.2396 2.77604 15.4062 3.32813C14.5729 3.88021 14 4.58333 13.6875 5.4375H11.3125C11 4.58333 10.4271 3.88021 9.59375 3.32813C8.76042 2.77604 7.85417 2.5 6.875 2.5C5.625 2.5 4.58333 2.91667 3.75 3.75C2.91667 4.58333 2.5 5.625 2.5 6.875C2.5 7.60417 2.64583 8.33854 2.9375 9.07812C3.22917 9.81771 3.75 10.6615 4.5 11.6094C5.25 12.5573 6.27083 13.6719 7.5625 14.9531C8.85417 16.2344 10.5 17.7708 12.5 19.5625Z" fill="#004872"/></svg></a>'

            }
            result += '<a href="/details/' + book.id + '">'
            result += '<div class="book-img text-center position-relative">'
            var url = book.bookImage.url ? book.bookImage.url : '/static/img/placeholder.png'
            result += '<img class="book-image" src="' + url + '" alt="' + book.title + '">'
            if (book.discountPercentage) {
              result += '<div class="book-img-dis-percentage position-absolute font-12 weight-500">' + book.discountPercentage + '% OFF</div>'

            }
            result += '</div>'
            result += '<div class="book-title weight-700 font-20 color-004872">' + book.title + '</div>'
            result += '<div class="book-author weight-400 font-16 color-gray">' + book.author + '</div>'
            result += '<div class="book-price weight-400 font-16 color-gray">MRP Rs. ' + book.price + '</div>'
            result += '<div class="book-best-price weight-400 font-16 color-gray">Best Price* <span class="book-best-price-value color-red weight-500">Rs ' + book.discountPrice + '</span></div>'
            result += '<div class="book-status color-red weight-400 font-16">New Book'
            result += '</div></a>'
            result += '<div class="book-add-to-cart">'
            if (userCart.includes(book.id)) {
              result += '<a href="/cart/" class="d-inline-block weight-500 font-20">Go to Cart</a>'
            } else {
              result += '<a class="add-to-cart font-20 color-white weight-500" href="/cart/add/" data-book-id="' + book.id + '">Add to Cart</a>'
            }
            console.log("result", result);
            result += '</div></div></div>'
          }
          result += "</div>"
          document.querySelector(".book-data").innerHTML = result;
        } else {
          // var aMessage = '<div class="alert alert-danger alert-dismissible fade show" role="alert">' +
          //   res.message + '<button type="button" class="btn-close" data-bs-dismiss="alert" aria-label="Close"></button>'
          // $(".messages").append(aMessage);
          document.querySelector(".book-data").innerHTML =res.message;
        }
      },
      complete: function () {

        // document.querySelector(".outer-rim").classList.add("hide");
      },
      error: function (res) {
        console.error(res.statusText);
        // document.querySelector(".outer-rim").classList.add("hide");
      },
    });
  })
  $(document).on("click", ".mobile-category-filter", function () {
    $(".categoy-filter").toggle()
  })
})(jQuery)
);
