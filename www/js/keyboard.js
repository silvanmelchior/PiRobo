var keytable = {
	'w': false,
	'a': false,
	's': false,
	'd': false,
	'i': false,
	'j': false,
	'k': false,
	'l': false,
	'0': false,
	'1': false,
	'2': false,
	'3': false,
	'4': false,
	'5': false,
	'6': false,
	'7': false,
	'8': false,
	'9': false
}

var col_no = '#EEE'
var col_yes = '#AAA'

var next_cmd = ""
var last_cmd = ""


function keyupdate() {
  for(var k in keytable) {
    if(keytable.hasOwnProperty(k)) {
      document.getElementById("key_" + k).style.backgroundColor = keytable[k] ? col_yes : col_no
    }
  }
  queue_cmd("k " +
    (keytable['w'] ? '1' : '0') + 
    (keytable['a'] ? '1' : '0') + 
    (keytable['s'] ? '1' : '0') + 
    (keytable['d'] ? '1' : '0') + 
    (keytable['i'] ? '1' : '0') + 
    (keytable['j'] ? '1' : '0') + 
    (keytable['k'] ? '1' : '0') + 
    (keytable['l'] ? '1' : '0') + 
    (keytable['0'] ? '1' : '0') + 
    (keytable['1'] ? '1' : '0') + 
    (keytable['2'] ? '1' : '0') + 
    (keytable['3'] ? '1' : '0') + 
    (keytable['4'] ? '1' : '0') + 
    (keytable['5'] ? '1' : '0') + 
    (keytable['6'] ? '1' : '0') + 
    (keytable['7'] ? '1' : '0') + 
    (keytable['8'] ? '1' : '0') + 
    (keytable['9'] ? '1' : '0')
  )
}

function keydown(e) {
  if(keytable.hasOwnProperty(e.key)) {
    keytable[e.key] = true
    keyupdate()
  }
}

function keyup(e) {
  if(keytable.hasOwnProperty(e.key)) {
    keytable[e.key] = false
    keyupdate()
  }
}

function keytouchstart(e) {
  var target = e.target.id.split('_')[1]
  keytable[target] = true
  keyupdate()
  return false
}

function keytouchend(e) {
  var target = e.target.id.split('_')[1]
  keytable[target] = false
  keyupdate()
  return false
}

function queue_cmd(cmd) {
	next_cmd = cmd;
}

function send_cmd() {
	if(next_cmd != last_cmd) {
		last_cmd = next_cmd
		var xhttp = new XMLHttpRequest()
		xhttp.open("POST", "cmd.php", true)
		xhttp.setRequestHeader("Content-type", "application/x-www-form-urlencoded")
		xhttp.send("ts=" + (new Date).getTime() + "&cmd=" + last_cmd)
	}
}


document.onkeydown = keydown
document.onkeyup = keyup
$('.touch_key').bind('touchstart', keytouchstart);
$('.touch_key').bind('touchend', keytouchend);
setInterval(send_cmd, 50)
