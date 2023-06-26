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
    var pickup = document.getElementById("id_pickup").value
    if (pickup == "self") {
        $(".addressList").css("display", "none")
    }else{
        $(".addressList").css("display", "block")
    }
    $(document).on("change", "#id_pickup", function(params) {
        params.preventDefault()
        if (this.value == "self") {
            $(".addressList").css("display", "none")
        }else{
            $(".addressList").css("display", "block")
        }
    })
  })(jQuery)
);
