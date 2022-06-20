document.addEventListener("DOMContentLoaded", function() {

  // $(".dropdown-trigger").dropdown();
  var pdf_pages_nav_bar = document.querySelectorAll('a.dropdown-trigger');
  pdf_pages_nav_bar.forEach((item, index) => {
    M.Dropdown.init(item, {hover: false});

    // console.log(index + " initiated :)");
  })

});
