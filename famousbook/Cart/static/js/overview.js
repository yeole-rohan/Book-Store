var $ = jQuery.noConflict();
$(document).ready((function () {
    var charge = document.getElementById("id_charges").value
    var chargeDiv = document.querySelector(".charge")
    if (charge) {
        if (charge === "40") {
            chargeDiv.innerHTML = "<div>Shipping Charges will be added Rs40</div>"
        } else if (charge == "50") {
            chargeDiv.innerHTML = "<div>Shipping Charges will be added Rs50</div>"
        } else if (this.value == "70") {
            chargeDiv.innerHTML = "<div>Shipping Charges will be added Rs70</div>"
        }else{
            chargeDiv.innerHTML = "<div>Please enquire about after payment</div>"
        }
        $(document).on("change", "#id_charges", function (params) {
            params.preventDefault()
            if (this.value == "40") {
                chargeDiv.innerHTML = "<div>Shipping Charges will be added Rs40</div>"
            } else if (this.value == "50") {
                chargeDiv.innerHTML = "<div>Shipping Charges will be added Rs50</div>"
            } else if (this.value == "70") {
                chargeDiv.innerHTML = "<div>Shipping Charges will be added Rs70</div>"
            }else{
                chargeDiv.innerHTML = "<div>Please enquire about after payment</div>"
            }
            
            $.ajax({
                url: "/cart/update/ship-charge/",
                data: {
                  ch: this.value,
                  csrfmiddlewaretoken: $("input[name=csrfmiddlewaretoken]").val(),
                },
                type: "POST",
                dataType: "json",
                success: function (res, status) {
                  if (res.success) {
                    var aMessage = '<div class="alert alert-success alert-dismissible fade show" role="alert">'+
                    res.message +'<button type="button" class="btn-close" data-bs-dismiss="alert" aria-label="Close"></button>'
                    $(".messages").append(aMessage);
                    window.location.reload(true)
      
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
        });
    }
})(jQuery)
);
