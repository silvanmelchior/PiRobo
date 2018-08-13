var block_output = false;
var output = "";

function compile() {
  block_output = true;
  $("#output_section").html("Compiling...<br>");
  
  $.get("compile.php?"+ new Date(),
    function(data) {
      $("#output_section").append(data);
    }
  );
}


function run() {
  $.get("run.php?"+ new Date());
  block_output = false;
  setTimeout('$("#output_section").html(output);', 500);
}


function stop() {
  $.get("stop.php?"+ new Date());
}


function update_done(res) {

  var msg = JSON.parse(res)
  
  var running = true
  if(msg.data.slice(-15) == "<19853732 stop>") running = false

  if(running) {
    block_output = false;
    output = msg.data;
    $("#run_btn").prop("disabled", true);
    $("#stop_btn").prop("disabled", false);
    $("#compile_btn").prop("disabled", true);
  }
  else {
    output = msg.data.slice(0,-15);
    $("#run_btn").prop("disabled", false);  
    $("#stop_btn").prop("disabled", true);
    $("#compile_btn").prop("disabled", false);
  }

  if(!block_output) $("#output_section").html(output);
    
  update(msg.hash);
  
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
