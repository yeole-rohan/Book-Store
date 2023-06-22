var $ = jQuery.noConflict();
$(document).ready((function () {
    /**
     * Attaches an event listener to the document that listens for changes to the quantity select
     * element with the class "delete-qty-select". When a change is detected, an AJAX request is sent
     * to the server to update the quantity of the item in the cart. If the request is successful, a
     * success message is displayed. If the request fails, an error message is displayed.
     * @param {object} params - The event object.
     * @returns None
     */
    $(document).on("change", ".delete-qty-select select", function(params) {
        params.preventDefault()
        $.ajax({
          url: "/cart/update/quantity/",
          data: {
            cartId: this.dataset.cart,
            qty: this.value,
            csrfmiddlewaretoken: $("input[name=csrfmiddlewaretoken]").val(),
          },
          type: "POST",
          dataType: "json",
          success: function (res, status) {
            if (res.success) {
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
            console.error(res.status);
          },
        });
    })
  })(jQuery)
);
