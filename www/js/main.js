var block_output = false;
var output = "";
var view_cam = false;
var x_finger_bak = null
var y_finger_bak = null
var x_obj_bak = 60
var y_obj_bak = 60


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


function toggle_cam() {
  if(view_cam) {
    document.getElementById("cam_pic").src = ""
    $('#collapseCam').collapse('hide');
    view_cam = false
  }
  else {
    document.getElementById("cam_pic").src = "/cam_interface/cam_pic_new.php?pDelay=50000"
    $('#collapseCam').collapse('show');
    view_cam = true
  }
}


function toggle_touch() {
  $('#collapseTouch').collapse('toggle');
}


function toggle_key() {
  $('#collapseKey').collapse('toggle');
}


function toggle_out() {
  $('#collapseOut').collapse('toggle');
}


function touchstart(e) {
	x_finger_bak = e.changedTouches[0].screenX
	y_finger_bak = e.changedTouches[0].screenY
	return false
}

function touchmove(e) {
	clipped = pos_clip(e)
	pos_ctrl(clipped[0], clipped[1])
	x = Math.floor(clipped[0]*100/120)
	y = Math.floor(clipped[1]*100/120)
	queue_cmd("t " + x + " " + y)
	return false
}

function touchend(e) {
	pos_ctrl(x_obj_bak, y_obj_bak)
	queue_cmd("t 50 50")
	return false
}

function pos_clip(e) {
	var new_x = e.changedTouches[0].screenX - x_finger_bak + x_obj_bak
	var new_y = e.changedTouches[0].screenY - y_finger_bak + y_obj_bak
	if(new_x < 0) new_x = 0
	if(new_y < 0) new_y = 0
	if(new_x > 120) new_x = 120
	if(new_y > 120) new_y = 120
	return [new_x,new_y]
}

function pos_ctrl(x, y) {
	document.getElementById("touch_ctrl").style.top =  y + 'px'
	document.getElementById("touch_ctrl").style.left = x + 'px'
}


update('');
toggle_cam();
pos_ctrl(x_obj_bak, y_obj_bak)
document.getElementById("touch_input_area").ontouchstart = touchstart
document.getElementById("touch_input_area").ontouchmove = touchmove
document.getElementById("touch_input_area").ontouchend = touchend

