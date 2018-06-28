<?php

	$socket = socket_create(AF_INET, SOCK_STREAM, SOL_TCP);
	$result = socket_connect($socket, 'localhost', 56000+10);
	socket_write($socket, $_POST['cmd'], strlen($_POST['cmd']));
	socket_close($socket);

?>
