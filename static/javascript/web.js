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







// function myFunction() {
//   var f = document.getElementById("customFile");
//   if (f.checkValidity()) {
//     alert("File upload succesfull. Please wait for few seconds.");
//   }
// }