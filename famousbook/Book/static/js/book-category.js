var $ = jQuery.noConflict();
$(document).ready((function () {
    $(document).on("click", "input[type='checkbox']", function(){
        console.log(this.value, this);
        
    })
  })(jQuery)
);
