var f = document.getElementById("customFile");

function myFunction() {
  if (f.checkValidity()) {
    alert("File upload succesfull! Please wait for 2 mins.");
  }
}
