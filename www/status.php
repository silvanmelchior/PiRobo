<?php

  for($i=0; $i<50; $i++) {

    # read data
	  $socket = socket_create(AF_INET, SOCK_STREAM, SOL_TCP);
	  socket_connect($socket, 'localhost', 56000);
	  socket_write($socket, "get", 3);
	  $msg = socket_read($socket, 10240);
	  socket_close($socket);
	
	  # calc hash
	  $hash = hash("md5", $msg);
    if($hash == $_GET["hash"]) {
      usleep(100000);
      continue;
    }
    
  }

  # output result
  $data = array('data' => $msg, 'hash' => $hash);
  echo json_encode($data);

?>
