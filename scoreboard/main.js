function reload_table() {

  var xhttp = new XMLHttpRequest();
  xhttp.onreadystatechange = function() {
    if(this.readyState == 4 && this.status == 200) {
      document.getElementById("table_out").innerHTML = this.responseText;
    }
  };
  xhttp.open("GET", "index.php?ajax", true);
  xhttp.send();

}

function remove_hint() {
  document.getElementById("pwd_msg").innerHTML = "";
}
