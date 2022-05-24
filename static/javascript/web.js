document.getElementById("cardMultiple").style.display = "none";
document.getElementById("cardIndividual").style.display = "none";


function uploadPressed() {
  document.getElementById('btnFetch').innerHTML = '<span class="spinner-grow" role="status" aria-hidden="true"></span>';
  document.getElementById('btnFetch').disabled = true;

  var myToast = new bootstrap.Toast(document.getElementById("myToast"), {
    delay: 10000
  });
  myToast.show();

}


document.getElementById("btnMultiple").addEventListener("click", function() {
  document.getElementById("cardMultiple").style.display = "block";
  document.getElementById("cardIndividual").style.display = "none";
});

document.getElementById("btnIndividual").addEventListener("click", function() {
  document.getElementById("cardIndividual").style.display = "block";
  document.getElementById("cardMultiple").style.display = "none";
});

// Tooltip
// var tooltipTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="tooltip"]'))
// var tooltipList = tooltipTriggerList.map(function (tooltipTriggerEl) {
//   return new bootstrap.Tooltip(tooltipTriggerEl)
// })

// popovers initialization - on hover
$('[data-toggle="popover-hover"]').popover({
  html: true,
  trigger: 'hover',
  placement: 'bottom',
  content: function () { return '<img src="' + $(this).data('img') + '" />'; }
});

// popovers initialization - on click
$('[data-toggle="popover-click"]').popover({
  html: true,
  trigger: 'click',
  placement: 'bottom',
  content: function () { return '<img src="' + $(this).data('img') + '" />'; }
});






// function myFunction() {
//   var f = document.getElementById("customFile");
//   if (f.checkValidity()) {
//     alert("File upload succesfull. Please wait for few seconds.");
//   }
// }