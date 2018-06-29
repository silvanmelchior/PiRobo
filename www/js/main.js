var running = true

function compile() {
  $("#output_section").html("Compiling...<br>");
  
  $.get("compile.php?"+ new Date(),
    function(data) {
      $("#output_section").append(data);
    }
  );
}


function run() {
  running = true;
  $.get("run.php?"+ new Date());
}


function stop() {
  $.get("stop.php?"+ new Date());
}


function update_done(res) {

  var msg = JSON.parse(res)
  
  var new_running = true
  if(msg.data.slice(-15) == "<19853732 stop>") new_running = false
  
  if(new_running) $("#output_section").html(msg.data);
  else if(!new_running && running) $("#output_section").html(msg.data.slice(0,-15));
  
  if(new_running) {
    $("#run_btn").prop("disabled", true);
    $("#stop_btn").prop("disabled", false);
    $("#compile_btn").prop("disabled", true);
  }
  else {
    $("#run_btn").prop("disabled", false);  
    $("#stop_btn").prop("disabled", true);
    $("#compile_btn").prop("disabled", false);
  }

  update(msg.hash);
  running = new_running
  
}


function update(hash) {
  $.ajax({
    url: "status.php",
    data: "hash="+hash,
    success: update_done,
    error: function() {setTimeout("update('')", 2000)}
  });
}


update('');
