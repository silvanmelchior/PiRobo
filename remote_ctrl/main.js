function discover() {

  var xhttp = new XMLHttpRequest();
  xhttp.onreadystatechange = function() {
    if(this.readyState == 4 && this.status == 200) {
      data = JSON.parse(this.responseText);
      html = "<table border=1 cellpadding=3>";
      html += "<tr><th>IP</th><th>SW Version</th><th>HW ID</th></tr>";
      for(i=0; i<data.length; i++) {
        html += "<tr>";
        html += "<td><a href=\"http://" + data[i].ip + "/\">" + data[i].ip + "</a></td>";
        html += "<td>" + data[i].sw_version + "</td>";
        html += "<td>" + data[i].hw_id + "</td>";
        html += "</tr>";
      }
      html += "</table>";
      document.getElementById("table_out").innerHTML = html;
    }
  };
  xhttp.open("GET", "discover.php", true);
  xhttp.send();

}

function shutdown_all() {

  if(confirm("Shutdown all robots?")) {  
    var xhttp = new XMLHttpRequest();
    xhttp.open("GET", "msg.php?msg=PiRobo+halt", true);
    xhttp.send();
  }

}

function reboot_all() {

  if(confirm("Reboot all robots?")) {
    var xhttp = new XMLHttpRequest();
    xhttp.open("GET", "msg.php?msg=PiRobo+reboot", true);
    xhttp.send();  
  }

}
