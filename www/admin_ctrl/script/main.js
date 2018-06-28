//
// Variables
//
var keytable = {
	37: 'left',
	38: 'up',
	39: 'right',
	40: 'down'
}

var keypressed = {
	'left': false,
	'up': false,
	'right': false,
	'down': false
}

var x_finger_bak = null
var y_finger_bak = null
var x_obj_bak = 60
var y_obj_bak = 60

var next_cmd = ""
var last_cmd = ""

var tags = true


//
// Functions for keyboard
//
function keyupdate() {
	var col_no = '#EEE'
	var col_yes = '#AAA'

	document.getElementById("keyboard_up").style.backgroundColor =
		keypressed['up'] ? col_yes : col_no
	document.getElementById("keyboard_left").style.backgroundColor =
		keypressed['left'] ? col_yes : col_no
	document.getElementById("keyboard_down").style.backgroundColor =
		keypressed['down'] ? col_yes : col_no
	document.getElementById("keyboard_right").style.backgroundColor =
		keypressed['right'] ? col_yes : col_no

  if(keypressed['up'] && !keypressed['left'] && !keypressed['right'] && !keypressed['down'])
    queue_cmd("motor forward");
  else if(keypressed['up'] && keypressed['left'] && !keypressed['right'] && !keypressed['down'])
    queue_cmd("motor left");
  else if(keypressed['up'] && !keypressed['left'] && keypressed['right'] && !keypressed['down'])
    queue_cmd("motor right");
  else
    queue_cmd("motor stop");

}

function keydown(e) {
	keypressed[keytable[e.keyCode]] = true
	keyupdate()
	show_ctrl(false)
}

function keyup(e) {
	keypressed[keytable[e.keyCode]] = false
	keyupdate()
}


//
// Functions for touch
//
function touchstart(e) {
	x_finger_bak = e.changedTouches[0].screenX
	y_finger_bak = e.changedTouches[0].screenY
	show_ctrl(true)
	queue_cmd("touch start")
	return false
}

function touchmove(e) {
	clipped = pos_clip(e)
	pos_ctrl(clipped[0], clipped[1])
	queue_cmd(
		"touch move " +
		Math.floor(clipped[0]*100/120) + " " +
		Math.floor(clipped[1]*100/120))
	return false
}

function touchend(e) {
	pos_ctrl(x_obj_bak, y_obj_bak)
	queue_cmd("touch end")
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

function show_ctrl(touch) {
	document.getElementById("keyboard_up").style.opacity = touch ? 0 : 1
	document.getElementById("keyboard_left").style.opacity = touch ? 0 : 1
	document.getElementById("keyboard_down").style.opacity = touch ? 0 : 1
	document.getElementById("keyboard_right").style.opacity = touch ? 0 : 1
	document.getElementById("touch_ctrl").style.opacity = touch ? 1 : 0
	document.getElementById("input_area").style.border = touch ? '1px solid #BBB' : '1px solid #FFF'
}


//
// Communication
//
function queue_cmd(cmd) {
	next_cmd = cmd;
}

function send_cmd() {
	if(next_cmd != last_cmd) {
		last_cmd = next_cmd;
		console.log(last_cmd)
		var xhttp = new XMLHttpRequest();
		xhttp.open("POST", "cmd.php", true);
		xhttp.setRequestHeader("Content-type", "application/x-www-form-urlencoded")
		xhttp.send("ts=" + (new Date).getTime() + "&cmd=" + last_cmd)
	}
}


//
// Tag Detection
//
function tag_swap() {
  tags = tags ? false : true
  if(!tags) {
    document.getElementById("cam_pic").src = "/cam_interface/cam_pic_new.php?pDelay=100000"
    document.getElementById("tag_swap_link").innerText = "Enable Tag Detection"
  }
  if(tags) {
    document.getElementById("cam_pic").src = "/cam_interface/cam_pic_new_tags.php?pDelay=100000"
    document.getElementById("tag_swap_link").innerText = "Disable Tag Detection"
  }
}


//
// Function for init
//
function init() {
	pos_ctrl(x_obj_bak, y_obj_bak)
	document.onkeydown = keydown
	document.onkeyup = keyup
	document.getElementById("input_area").ontouchstart = touchstart
	document.getElementById("input_area").ontouchmove = touchmove
	document.getElementById("input_area").ontouchend = touchend
	setInterval(send_cmd, 100)
	tag_swap()
}
