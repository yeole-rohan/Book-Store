var $ = jQuery.noConflict();
$(document).ready((function () {
    $(document).on("click", "input[type='checkbox']", function(){
        console.log(this.value, this);
        
    })
    $(document).on("click", ".mobile-category-filter", function(){
      $(".categoy-filter").toggle()
      
  })
  })(jQuery)
);
