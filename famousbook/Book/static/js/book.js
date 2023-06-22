var $ = jQuery.noConflict();
$(document).ready((function () {
    $.ajax({
        url: "/get/primary-category/ajax/" + document.querySelector(".book-id").dataset.id + "/",
        type: "GET",
        dataType: "json",
        success: function (res, status) {
          if (res["status"] == "ok") {
            $(".primaryCategorySelect").select2({
              placeholder: "Select Labels", //placeholder
              data: res.label,
              allowClear: true,
              closeOnSelect: false,
              tags: true,
            });
            document.getElementById("id_primaryCategory").value =
              $(".primaryCategorySelect").val();
          }
        },
        error: function (res) {
          console.error(res.status);
        },
      });
      $('.primaryCategorySelect').on('change.select2', function (e) {
          document.getElementById('id_primaryCategory').value = $(".primaryCategorySelect").val()
      });
  })(jQuery)
);
