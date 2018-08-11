//
// Variables
//
var keytable = {
	37: 'left',
	38: 'up',
	39: 'right',
	40: 'down',
	87: 'w',
	65: 'a',
	83: 's',
	68: 'd'
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
var pan = 0.5
var tilt = 0.5
var pan_bak = 0.5
var tilt_bak = 0.5
var servo_steps = 0.05
var servo_divider = 500

var next_cmd_motor = ""
var last_cmd_motor = ""
var next_cmd_servo = ""
var last_cmd_servo = ""



//
// Functions for keyboard
//
function motor_update() {
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
    queue_cmd_motor("motor 1 1");
  else if(keypressed['up'] && keypressed['left'] && !keypressed['right'] && !keypressed['down'])
    queue_cmd_motor("motor 0 1");
  else if(keypressed['up'] && !keypressed['left'] && keypressed['right'] && !keypressed['down'])
    queue_cmd_motor("motor 1 0");
  else if(!keypressed['up'] && keypressed['left'] && !keypressed['right'] && !keypressed['down'])
    queue_cmd_motor("motor -1 1");
  else if(!keypressed['up'] && !keypressed['left'] && keypressed['right'] && !keypressed['down'])
    queue_cmd_motor("motor 1 -1");
  else if(!keypressed['up'] && !keypressed['left'] && !keypressed['right'] && keypressed['down'])
    queue_cmd_motor("motor -1 -1");
  else if(!keypressed['up'] && keypressed['left'] && !keypressed['right'] && keypressed['down'])
    queue_cmd_motor("motor 0 -1");
  else if(!keypressed['up'] && !keypressed['left'] && keypressed['right'] && keypressed['down'])
    queue_cmd_motor("motor -1 0");
  else
    queue_cmd_motor("motor 0 0");

}

function servo_update() {
  queue_cmd_servo("servo " + pan + " " + tilt)
}

function keydown(e) {
  // servo
  if(keytable[e.keyCode] == 's' && !keypressed['s']) {
    if(tilt <= 1-servo_steps) {
      tilt += servo_steps
      servo_update()
    }
  }
  if(keytable[e.keyCode] == 'd' && !keypressed['d']) {
    if(pan >= servo_steps) {
      pan -= servo_steps
      servo_update()
    }
  }
  if(keytable[e.keyCode] == 'w' && !keypressed['w']) {
    if(tilt >= servo_steps) {
      tilt -= servo_steps
      servo_update()
    }
  }
  if(keytable[e.keyCode] == 'a' && !keypressed['a']) {
    if(pan <= 1-servo_steps) {
      pan += servo_steps
      servo_update()
    }
  }
  
  // motor
	keypressed[keytable[e.keyCode]] = true
	motor_update()
	show_ctrl(false)
}

function keyup(e) {
	keypressed[keytable[e.keyCode]] = false
	motor_update()
}



//
// Functions for motor touch
//
function touchstart(e) {
	x_finger_bak = e.changedTouches[0].screenX
	y_finger_bak = e.changedTouches[0].screenY
	show_ctrl(true)
	return false
}

function touchmove(e) {
	clipped = pos_clip(e)
	pos_ctrl(clipped[0], clipped[1])
	x = clipped[0]*100/120
	y = clipped[1]*100/120
  if(y <= 50) {
    speed = (50-y)/50
    sign = 1
  }
  else {
    speed = (y-50)/50
    sign = -1
  }
  l = Math.min(1,1 - (50-x)/50)
  r = Math.min(1,1 - (x-50)/50)
  l *= speed*sign
  r *= speed*sign
	queue_cmd_motor("motor " + l + " " + r)
	return false
}

function touchend(e) {
	pos_ctrl(x_obj_bak, y_obj_bak)
	queue_cmd_motor("motor 0 0")
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
// Functions for servo touch
//
function servostart(e) {
	x_finger_bak = e.changedTouches[0].screenX
	y_finger_bak = e.changedTouches[0].screenY
	return false
}

function servomove(e) {
	diff_x = e.changedTouches[0].screenX - x_finger_bak
	diff_y = e.changedTouches[0].screenY - y_finger_bak

  pan = pan_bak + diff_x/servo_divider
  tilt = tilt_bak - diff_y/servo_divider
  if(pan >= 1) pan = 1
  else if(pan <= 0) pan = 0
  if(tilt >= 1) tilt = 1
  else if(tilt <= 0) tilt = 0
  servo_update()
	
	return false
}

function servoend(e) {
  pan_bak = pan
  tilt_bak = tilt
	return false
}



//
// Functions for communication
//
function queue_cmd_motor(cmd) {
	next_cmd_motor = cmd
}

function queue_cmd_servo(cmd) {
	next_cmd_servo = cmd
}

function send_cmd() {
	if(next_cmd_motor != last_cmd_motor) {
		last_cmd_motor = next_cmd_motor
		var xhttp = new XMLHttpRequest()
		xhttp.open("POST", "cmd.php", true)
		xhttp.setRequestHeader("Content-type", "application/x-www-form-urlencoded")
		xhttp.send("ts=" + (new Date).getTime() + "&cmd=" + last_cmd_motor)
	}
	if(next_cmd_servo != last_cmd_servo) {
		last_cmd_servo = next_cmd_servo
		var xhttp = new XMLHttpRequest()
		xhttp.open("POST", "cmd.php", true)
		xhttp.setRequestHeader("Content-type", "application/x-www-form-urlencoded")
		xhttp.send("ts=" + (new Date).getTime() + "&cmd=" + last_cmd_servo)
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
	document.getElementById("cam_pic").ontouchstart = servostart
	document.getElementById("cam_pic").ontouchmove = servomove
	document.getElementById("cam_pic").ontouchend = servoend
	document.getElementById("cam_pic").src = "/cam_interface/cam_pic_new.php?pDelay=50000"
	setInterval(send_cmd, 100)
}
