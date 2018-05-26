<!DOCTYPE html>
<html>
	<head>
		<meta charset="utf-8"> 
		<meta name="author" content="Silvan Melchior">
		<meta name="viewport" content="width=device-width, initial-scale=1">
		<title>PiRobo Ctrl</title>
		<link href="style/main.css?v=1" rel="stylesheet" type="text/css" />
		<script src="script/main.js?v=1"></script>
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
		<center>
  		<a id="tag_swap_link" href="javascript:tag_swap();"></a>
		</center>
		<br><br>
	</body>
	<script>init()</script>
</html>
