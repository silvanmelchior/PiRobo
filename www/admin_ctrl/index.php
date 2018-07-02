<!DOCTYPE html>
<html>
	<head>
		<meta charset="utf-8"> 
		<meta name="author" content="Silvan Melchior">
		<meta name="viewport" content="width=device-width, initial-scale=1">
		<title>PiRobo Ctrl</title>
		<link href="style/main.css?v=2" rel="stylesheet" type="text/css" />
		<script src="script/main.js?v=2"></script>
	</head>

	<body>
		<center>
			<h1>PiRobo Admin Ctrl</h1>
		</center>
		<img id="cam_pic">
		<div id="input_area">
			<div id="keyboard_up">&uarr;</div>
			<div id="keyboard_left">&larr;</div>
			<div id="keyboard_down">&darr;</div>
			<div id="keyboard_right">&rarr;</div>
			<div id="touch_ctrl"></div>  		
		</div>
		<div id="expl_div">
		  <p>Keyboard: Use arrow keys to move roboter, use W,A,S,D to control servo.</p>
		  <p>Touchscreen: Use joystick to move roboter, drag camera image to control servo.</p>
		</div>
		<br><br>
	</body>
	<script>init()</script>
</html>
