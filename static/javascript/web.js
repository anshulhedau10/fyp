var f = document.getElementById("customFile");

function myFunction() {
  if (f.checkValidity()) {
    alert("File upload succesfull!");
  }
  else {
    alert("Please select a file!");
    return false;
  }
}