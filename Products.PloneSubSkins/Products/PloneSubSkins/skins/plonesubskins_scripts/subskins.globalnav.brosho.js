$(document).ready(function() {  
  $('#portal-globalnav li a, ').click(function() { //make the navigation links functional for the example pages
    document.location.href = $(this).attr('href');
  });
  $('#brosho').click(function() { //make brosho selection clickable
  });
});