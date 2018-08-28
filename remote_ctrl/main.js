var clients = null;
var view_toggle = true;
var text_hidden = false;

function discover() {

  var xhttp = new XMLHttpRequest();
  xhttp.onreadystatechange = function() {
    if(this.readyState == 4 && this.status == 200) {
      clients = JSON.parse(this.responseText);
      if(view_toggle) table_view();
      else camera_view();
    }
  };
  xhttp.open("GET", "discover.php", true);
  xhttp.send();

}

function table_view() {
  html = "<table border=1 cellpadding=3>";
  html += "<tr><th>Nr</th><th>IP</th><th>SW Version</th><th>HW ID</th></tr>";
  for(i=0; i<clients.length; i++) {
    html += "<tr>";
    html += "<td>" + (i+1) + "</td>";
    html += "<td><a href=\"http://" + clients[i].ip + "/\" target=\"_blank\">" + clients[i].ip + "</a></td>";
    html += "<td>" + clients[i].sw_version + "</td>";
    html += "<td>" + clients[i].hw_id + "</td>";
    html += "</tr>";
  }
  html += "</table>";
  if(!text_hidden) html += "<br><a href='javascript:camera_view()'>Camera View</a>";
  document.getElementById("table_out").innerHTML = html;
  view_toggle = true;
}

function camera_view() {
  html = "";
  for(i=0; i<clients.length; i++) {
    html += "<div class='client_div'><a href=\"http://" + clients[i].ip + "/\" target=\"_blank\">";
    html += "<img class='client_img' src=\"http://" + clients[i].ip + "/cam_interface/cam_pic_new.php?pDelay=100000\">";
    html += "</a></div>";
  }
  html += "</table>";
  if(!text_hidden) html += "<br><a href='javascript:table_view()'>Table View</a>";
  document.getElementById("table_out").innerHTML = html;
  view_toggle = false;
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

function hide_text() {

  document.getElementById("title").style.display = "none";
  document.getElementById("controls").style.display = "none";
  text_hidden = true;

}
